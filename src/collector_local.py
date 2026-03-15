"""
collector_local.py — Plan B: Read photos from local/rclone-mounted path
=====================================================================
Use case: Google Photos mounted via rclone (or any local folder)
Completely bypasses OAuth / Google Photos API entirely.

Setup (one-time, human does this):
  1. Install rclone: https://rclone.org/install/
  2. rclone config -> add remote "gphotos" (Google Photos type)
  3. Mount: rclone mount gphotos:album/ ~/mnt/gphotos --vfs-cache-mode full &
  4. Set LOCAL_PHOTOS_PATH in .env to the mount point (e.g. ~/mnt/gphotos)
     OR pass --path argument to override

Usage:
  python -m src.collector_local --test
  python -m src.collector_local --path /mnt/gphotos --limit 10
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.heif', '.mp4', '.mov', '.avi'}


def get_photos_path(override: str = None) -> Path:
    """Resolve local photos path: CLI arg > .env > default fallback."""
    if override:
        return Path(override).expanduser()
    
    # Try .env
    env_path = os.getenv('LOCAL_PHOTOS_PATH', '')
    if env_path:
        return Path(env_path).expanduser()
    
    # Default rclone mount points
    defaults = [
        Path.home() / 'mnt' / 'gphotos',
        Path.home() / 'gphotos',
        Path('/mnt/gphotos'),
    ]
    for p in defaults:
        if p.exists():
            logger.info(f'Auto-detected photos path: {p}')
            return p
    
    raise FileNotFoundError(
        'No local photos path found. Set LOCAL_PHOTOS_PATH in .env or use --path argument. '
        'If using rclone: rclone mount gphotos:album/ ~/mnt/gphotos --vfs-cache-mode full'
    )


def collect_media_items(base_path: Path, limit: int = None, recursive: bool = True) -> list:
    """
    Scan local path for media files. Returns list of dicts compatible with
    the original collector.py output format for downstream pipeline compatibility.
    """
    items = []
    
    if not base_path.exists():
        raise FileNotFoundError(f'Photos path does not exist: {base_path}')
    
    logger.info(f'Scanning: {base_path} (recursive={recursive})')
    
    pattern = '**/*' if recursive else '*'
    all_files = list(base_path.glob(pattern))
    media_files = [f for f in all_files if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
    
    logger.info(f'Found {len(media_files)} media files (from {len(all_files)} total files)')
    
    if limit:
        media_files = media_files[:limit]
        logger.info(f'Limited to {limit} items')
    
    for f in media_files:
        stat = f.stat()
        items.append({
            'id': str(f.relative_to(base_path)),       # relative path as ID
            'filename': f.name,
            'local_path': str(f.absolute()),
            'mime_type': _guess_mime(f.suffix),
            'size_bytes': stat.st_size,
            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'source': 'local',
        })
    
    return items


def _guess_mime(ext: str) -> str:
    mime_map = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
        '.gif': 'image/gif', '.webp': 'image/webp', '.heic': 'image/heic',
        '.heif': 'image/heif', '.mp4': 'video/mp4', '.mov': 'video/quicktime',
        '.avi': 'video/avi',
    }
    return mime_map.get(ext.lower(), 'application/octet-stream')


def main():
    parser = argparse.ArgumentParser(description='Local/rclone photo collector (Plan B)')
    parser.add_argument('--path', type=str, help='Override local photos path')
    parser.add_argument('--limit', type=int, default=None, help='Max items to collect (default: all)')
    parser.add_argument('--no-recursive', action='store_true', help='Disable recursive scan')
    parser.add_argument('--test', action='store_true', help='Test mode: scan and print summary only')
    args = parser.parse_args()
    
    try:
        base_path = get_photos_path(args.path)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    
    limit = 5 if args.test else args.limit
    recursive = not args.no_recursive
    
    items = collect_media_items(base_path, limit=limit, recursive=recursive)
    
    if args.test:
        print(f'\n=== Plan B (Local Source) Test Results ===')
        print(f'Path:  {base_path}')
        print(f'Found: {len(items)} items')
        for item in items[:5]:
            print(f'  - {item["filename"]} ({item["mime_type"]}, {item["size_bytes"]} bytes)')
        print('\n=> Plan B collector is working correctly.' if items else '\n=> No items found. Check path.')
    else:
        print(f'Collected {len(items)} items from {base_path}')
    
    return items


if __name__ == '__main__':
    main()
