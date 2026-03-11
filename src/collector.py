"""
Google Photos Collector Module
Fetches new photos from Google Photos (supports two accounts).

Phase: 1
Status: SKELETON — auth must work first

Key design decisions:
- Incremental: only fetches photos since last_run timestamp
- Deduplication: skips photo_ids already in processed_ids.json
- Two accounts: owner + spouse, merged into single stream
- Downloads to temp dir, caller responsible for cleanup
"""

import os
import logging
import tempfile
import requests
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from src.auth.google_auth import authenticate

logger = logging.getLogger('maplab.collector')

PHOTOS_API_BASE = "https://photoslibrary.googleapis.com/v1"


@dataclass
class PhotoRecord:
    """Represents a single photo ready for processing."""
    photo_id: str
    original_filename: str
    local_path: str
    captured_at: datetime
    width: int
    height: int
    account: str              # 'owner' or 'spouse'
    mime_type: str = "image/jpeg"
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    
    # Populated by downstream modules
    project_name: str = ""
    category: str = "other"
    keywords: list = field(default_factory=list)
    alt_text: str = ""
    drive_url: str = ""


def fetch_photos_for_account(
    account: str,
    since: Optional[datetime],
    processed_ids: list,
    limit: Optional[int] = None
) -> list[PhotoRecord]:
    """
    Fetch new photos for one account since given timestamp.
    
    Args:
        account: 'owner' or 'spouse'
        since: Only fetch photos after this datetime (None = last 7 days)
        processed_ids: Skip photos with these IDs
        limit: Max photos to fetch (None = all)
    
    Returns:
        List of PhotoRecord objects (photos downloaded to temp dir)
    """
    creds = authenticate(account)
    headers = {"Authorization": f"Bearer {creds.token}"}
    
    # Default window: last 7 days if no prior run
    if since is None:
        since = datetime.utcnow() - timedelta(days=7)
    
    # Build date filter for Photos API
    filter_body = {
        "dateFilter": {
            "ranges": [{
                "startDate": {
                    "year": since.year,
                    "month": since.month,
                    "day": since.day
                },
                "endDate": {
                    "year": datetime.utcnow().year,
                    "month": datetime.utcnow().month,
                    "day": datetime.utcnow().day
                }
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
                headers=headers,
                json=body,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Photos API error for {account}: {e}")
            break
        
        items = data.get("mediaItems", [])
        
        for item in items:
            photo_id = item["id"]
            
            # Skip already processed
            if photo_id in processed_ids:
                continue
            
            # Skip videos
            if not item.get("mimeType", "").startswith("image/"):
                continue
            
            # Download photo
            try:
                local_path = download_photo(item, headers)
            except Exception as e:
                logger.warning(f"Download failed for {photo_id}: {e}")
                continue
            
            # Parse metadata
            meta = item.get("mediaMetadata", {})
            captured_str = meta.get("creationTime", "")
            try:
                captured_at = datetime.fromisoformat(
                    captured_str.replace("Z", "+00:00")
                )
            except ValueError:
                captured_at = datetime.utcnow()
            
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
            logger.info(f"Queued: {record.original_filename} ({account})")
            
            if limit and len(photos) >= limit:
                logger.info(f"Limit reached ({limit})")
                return photos
        
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    
    return photos


def download_photo(item: dict, headers: dict) -> str:
    """Download photo to temp directory. Returns local file path."""
    # Photos API: append =d for download
    download_url = item["baseUrl"] + "=d"
    
    suffix = ".jpg"
    if "heic" in item.get("mimeType", "").lower():
        suffix = ".heic"
    
    tmp = tempfile.NamedTemporaryFile(
        suffix=suffix, delete=False,
        dir=Path("./temp"), prefix="maplab_"
    )
    
    Path("./temp").mkdir(exist_ok=True)
    
    response = requests.get(download_url, headers=headers, timeout=60, stream=True)
    response.raise_for_status()
    
    with open(tmp.name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return tmp.name


def collect_photos(
    since: Optional[datetime] = None,
    processed_ids: list = None,
    limit: Optional[int] = None,
    accounts: list = None
) -> list[PhotoRecord]:
    """
    Main collection function — fetches from all configured accounts.
    
    Args:
        since: Fetch photos after this datetime
        processed_ids: Skip these photo IDs
        limit: Max total photos (applied after merging accounts)
        accounts: Which accounts to fetch from (default: ['owner', 'spouse'])
    
    Returns:
        Merged, deduplicated list of PhotoRecord objects
    """
    if processed_ids is None:
        processed_ids = []
    if accounts is None:
        accounts = ['owner', 'spouse']
    
    all_photos = []
    
    for account in accounts:
        logger.info(f"Fetching from account: {account}")
        try:
            photos = fetch_photos_for_account(
                account=account,
                since=since,
                processed_ids=processed_ids,
                limit=limit
            )
            all_photos.extend(photos)
            logger.info(f"Got {len(photos)} photos from {account}")
        except Exception as e:
            logger.error(f"Failed to fetch from {account}: {e}")
    
    # Sort by capture time
    all_photos.sort(key=lambda p: p.captured_at)
    
    if limit:
        all_photos = all_photos[:limit]
    
    return all_photos


if __name__ == '__main__':
    # Quick test: fetch 1 photo from owner account
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--account', default='owner')
    args = parser.parse_args()
    
    print(f"Testing collector for: {args.account}")
    photos = collect_photos(
        accounts=[args.account],
        limit=1 if args.test else None
    )
    print(f"✓ Fetched {len(photos)} photos")
    for p in photos[:3]:
        print(f"  - {p.original_filename} | {p.captured_at} | {p.account}")
