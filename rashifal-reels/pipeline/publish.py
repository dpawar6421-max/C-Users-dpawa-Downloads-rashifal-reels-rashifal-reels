"""Upload each reel to S3-compatible storage (public URL), then publish to Instagram, one every GAP_MINUTES."""
import os, sys, time, requests, boto3
from common import load, notify

GRAPH = "https://graph.facebook.com/v21.0"
IG_ID, IG_TOKEN = os.environ["IG_USER_ID"], os.environ["IG_ACCESS_TOKEN"]
BUCKET, BASE = os.environ["S3_BUCKET"], os.environ["PUBLIC_BASE_URL"].rstrip("/")
GAP = int(os.getenv("GAP_MINUTES", "20"))
DRY = os.getenv("DRY_RUN") == "1"

s3 = boto3.client("s3", endpoint_url=os.getenv("S3_ENDPOINT") or None,
                  aws_access_key_id=os.getenv("S3_KEY"), aws_secret_access_key=os.getenv("S3_SECRET"),
                  region_name=os.getenv("S3_REGION", "auto"))

def upload(path, key):
    s3.upload_file(path, BUCKET, key, ExtraArgs={"ContentType": "video/mp4"})
    return f"{BASE}/{key}"

def post_reel(url, caption):
    r = requests.post(f"{GRAPH}/{IG_ID}/media", data={"media_type": "REELS", "video_url": url,
        "caption": caption, "share_to_feed": "true", "access_token": IG_TOKEN}, timeout=60).json()
    if "id" not in r: raise RuntimeError(f"Container failed: {r}")
    cid = r["id"]
    for _ in range(40):                      # wait up to ~10 minutes for processing
        time.sleep(15)
        st = requests.get(f"{GRAPH}/{cid}", params={"fields": "status_code", "access_token": IG_TOKEN}, timeout=30).json()
        if st.get("status_code") == "FINISHED": break
        if st.get("status_code") == "ERROR": raise RuntimeError(f"Processing error: {st}")
    else:
        raise RuntimeError("Processing timeout")
    pub = requests.post(f"{GRAPH}/{IG_ID}/media_publish", data={"creation_id": cid, "access_token": IG_TOKEN}, timeout=60).json()
    if "id" not in pub: raise RuntimeError(f"Publish failed: {pub}")
    return pub["id"]

def main():
    date = sys.argv[1]
    data = load(f"out/{date}/content.json")
    failed = []
    for n, it in enumerate(data["rashis"]):
        path = f"out/{date}/reel_{it['index']}.mp4"
        if not os.path.exists(path):
            failed.append(it["name"]); continue
        try:
            url = upload(path, f"rashifal/{date}/reel_{it['index']}.mp4")
            if DRY: print("DRY RUN, would post", url); continue
            post_reel(url, it["caption"])
            print("Posted", it["name"])
        except Exception as e:
            failed.append(it["name"]); notify(f"❌ {it['name']} reel failed: {e}")
        if n < 11 and not DRY: time.sleep(GAP * 60)
    notify(f"✅ {date}: {12-len(failed)}/12 reels posted." + (f" Failed: {', '.join(failed)}" if failed else ""))
    if failed: sys.exit(1)

if __name__ == "__main__":
    main()
