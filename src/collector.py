"""
Google Photos Collector Module
Fetches new photos from Google Photos (supports two accounts).

Phase: 1
Status: ACTIVE - owner OAuth confirmed, spouse optional

Key design decisions:
- Incremental: only fetches photos since last_run timestamp
- Default window: last 30 days (widened for first run)
- Deduplication: skips photo_ids already in processed_ids
- Two accounts: owner + spouse (spouse optional, skipped if token missing)
- Downloads to temp dir, caller responsible for cleanup
"""

import os
import logging
import tempfile
import requests
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from src.auth.google_auth import authenticate

logger = logging.getLogger('maplab.collector')

PHOTOS_API_BASE = "https://photoslibrary.googleapis.com/v1"
DEFAULT_SINCE_DAYS = 30


@dataclass
class PhotoRecord:
    photo_id: str
    original_filename: str
    local_path: str
    captured_at: datetime
    width: int
    height: int
    account: str
    mime_type: str = "image/jpeg"
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    project_name: str = ""
    category: str = "other"
    keywords: list = field(default_factory=list)
    alt_text: str = ""
    drive_url: str = ""


def fetch_photos_for_account(account, since, processed_ids, limit=None):
    try:
        creds = authenticate(account)
    except FileNotFoundError as e:
        logger.warning(f"[{account}] Token not found - skipping: {e}")
        return []
    except Exception as e:
        logger.error(f"[{account}] Auth failed - skipping: {e}")
        return []

    headers = {"Authorization": f"Bearer {creds.token}"}
    now = datetime.now(timezone.utc)

    if since is None:
        since = now - timedelta(days=DEFAULT_SINCE_DAYS)
    elif isinstance(since, str):
        since = datetime.fromisoformat(since)
    if since.tzinfo is None:
        since = since.replace(tzinfo=timezone.utc)

    logger.info(f"[{account}] Fetching since {since.date()} to {now.date()}")

    filter_body = {
        "dateFilter": {
            "ranges": [{
                "startDate": {"year": since.year, "month": since.month, "day": since.day},
                "endDate": {"year": now.year, "month": now.month, "day": now.day}
            }]
        }
    }

    photos = []
    next_page_token = None

    while True:
        body = {"pageSize": 100, "filters": filter_body}
        if next_page_token:
            body["pageToken"] = next_page_token

        try:
            response = requests.post(
                f"{PHOTOS_API_BASE}/mediaItems:search",
                headers=headers, json=body, timeout=30
            )
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError as e:
            logger.error(f"[{account}] HTTP {e} - {response.text[:300]}")
            break
        except requests.RequestException as e:
            logger.error(f"[{account}] Request error: {e}")
            break

        items = data.get("mediaItems", [])
        logger.info(f"[{account}] API returned {len(items)} items (keys: {list(data.keys())})")

        for item in items:
            photo_id = item["id"]
            if photo_id in processed_ids:
                continue
            if not item.get("mimeType", "").startswith("image/"):
                continue
            try:
                local_path = download_photo(item, headers)
            except Exception as e:
                logger.warning(f"Download failed {photo_id}: {e}")
                continue

            meta = item.get("mediaMetadata", {})
            try:
                captured_at = datetime.fromisoformat(meta.get("creationTime", "").replace("Z", "+00:00"))
            except ValueError:
                captured_at = datetime.now(timezone.utc)

            record = PhotoRecord(
                photo_id=photo_id,
                original_filename=item.get("filename", f"{photo_id}.jpg"),
                local_path=local_path,
                captured_at=captured_at,
                width=int(meta.get("width", 0)),
                height=int(meta.get("height", 0)),
                account=account,
                mime_type=item.get("mimeType", "image/jpeg")
            )
            photos.append(record)
            logger.info(f"[{account}] Queued: {record.original_filename}")

            if limit and len(photos) >= limit:
                return photos

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return photos


def download_photo(item, headers):
    download_url = item["baseUrl"] + "=d"
    mime = item.get("mimeType", "").lower()
    suffix = ".heic" if "heic" in mime else ".png" if "png" in mime else ".jpg"

    Path("./temp").mkdir(exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False, dir="./temp", prefix="maplab_")

    r = requests.get(download_url, headers=headers, timeout=60, stream=True)
    r.raise_for_status()
    with open(tmp.name, 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return tmp.name


def collect_photos(since=None, processed_ids=None, limit=None, accounts=None, target_date=None):
    if processed_ids is None:
        processed_ids = []
    if accounts is None:
        accounts = ['owner']

    if target_date:
        try:
            since = datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            logger.warning(f"Invalid target_date: {target_date}")

    all_photos = []
    for account in accounts:
        logger.info(f"Fetching from: {account}")
        try:
            photos = fetch_photos_for_account(account, since, processed_ids, limit)
            all_photos.extend(photos)
            logger.info(f"Got {len(photos)} from {account}")
        except Exception as e:
            logger.error(f"Failed {account}: {e}", exc_info=True)

    all_photos.sort(key=lambda p: p.captured_at)
    if limit:
        all_photos = all_photos[:limit]

    logger.info(f"Total: {len(all_photos)} photos from {accounts}")
    return all_photos


if __name__ == '__main__':
    import argparse
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--account', default='owner')
    parser.add_argument('--days', type=int, default=30)
    args = parser.parse_args()

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    photos = collect_photos(since=since, accounts=[args.account], limit=1 if args.test else None)
    print(f"Fetched {len(photos)} photos")
    for p in photos[:3]:
        print(f"  - {p.original_filename} | {p.captured_at.date()} | {p.account}")
