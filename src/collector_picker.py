"""
collector_picker.py — Plan A: Google Photos Picker API
=====================================================
Replaces photoslibrary.readonly (deprecated 2025-03-31) with
the new Picker API (photospicker.mediaitems.readonly).

Flow (semi-interactive, one-time per session):
  1. Script creates a Picker Session via POST /v1/sessions
  2. Script opens pickerUri in browser for user to select photos
  3. Script polls session until user completes selection
  4. Script lists selected MediaItems and returns them

API Reference: https://developers.google.com/photos/picker/reference/rest
Scope: https://www.googleapis.com/auth/photospicker.mediaitems.readonly
Endpoint: https://photospicker.googleapis.com/v1/sessions

NOTE: Picker API requires user interaction each run (they select photos in browser).
      For fully automated pipeline use Plan B (collector_local.py) instead.
"""

import os
import sys
import time
import webbrowser
import argparse
import logging
import json
import requests
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# NEW scope — replaces photoslibrary.readonly which was removed 2025-03-31
SCOPES = ['https://www.googleapis.com/auth/photospicker.mediaitems.readonly']

PICKER_BASE = 'https://photospicker.googleapis.com/v1'
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'auth/credentials.json')
TOKEN_FILE = os.getenv('PICKER_TOKEN_FILE', 'auth/token_picker.json')


def get_credentials() -> Credentials:
    """OAuth2 flow for Picker API scope."""
    creds = None
    
    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not Path(CREDENTIALS_FILE).exists():
                raise FileNotFoundError(
                    f'credentials.json not found at {CREDENTIALS_FILE}. '
                    'Run auth/setup_credentials.py first.'
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        logger.info(f'Token saved to {TOKEN_FILE}')
    
    return creds


def create_session(creds: Credentials) -> dict:
    """Create a new Picker session. Returns session object with pickerUri."""
    headers = {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}
    resp = requests.post(f'{PICKER_BASE}/sessions', headers=headers, json={})
    resp.raise_for_status()
    session = resp.json()
    logger.info(f'Session created: {session.get("id")}')
    return session


def poll_session(creds: Credentials, session_id: str, timeout_seconds: int = 300) -> bool:
    """Poll until user finishes selecting photos or timeout."""
    headers = {'Authorization': f'Bearer {creds.token}'}
    start = time.time()
    
    while time.time() - start < timeout_seconds:
        resp = requests.get(f'{PICKER_BASE}/sessions/{session_id}', headers=headers)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('mediaItemsSet'):
            logger.info('User completed photo selection.')
            return True
        
        poll_interval = data.get('pollingConfig', {}).get('pollInterval', 5)
        # Convert protobuf duration string "5s" to int
        if isinstance(poll_interval, str):
            poll_interval = int(poll_interval.replace('s', '').split('.')[0])
        
        logger.info(f'Waiting for selection... (polling every {poll_interval}s)')
        time.sleep(poll_interval)
    
    logger.warning('Timed out waiting for user selection.')
    return False


def list_media_items(creds: Credentials, session_id: str) -> list:
    """List all media items selected in this session."""
    headers = {'Authorization': f'Bearer {creds.token}'}
    items = []
    page_token = None
    
    while True:
        params = {'sessionId': session_id, 'pageSize': 100}
        if page_token:
            params['pageToken'] = page_token
        
        resp = requests.get(f'{PICKER_BASE}/mediaItems', headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        batch = data.get('mediaItems', [])
        items.extend(batch)
        logger.info(f'Fetched {len(batch)} items (total so far: {len(items)})')
        
        page_token = data.get('nextPageToken')
        if not page_token:
            break
    
    return items


def delete_session(creds: Credentials, session_id: str):
    """Clean up session after use (best practice per Google docs)."""
    headers = {'Authorization': f'Bearer {creds.token}'}
    resp = requests.delete(f'{PICKER_BASE}/sessions/{session_id}', headers=headers)
    if resp.status_code == 200:
        logger.info(f'Session {session_id} deleted.')
    else:
        logger.warning(f'Could not delete session: {resp.status_code}')


def run_picker_flow(test: bool = False, limit: int = None) -> list:
    """Full Picker API flow: auth -> session -> user picks -> fetch items."""
    creds = get_credentials()
    session = create_session(creds)
    session_id = session['id']
    picker_uri = session['pickerUri']
    
    print(f'\n=== Open this URL to select photos ===')
    print(f'{picker_uri}')
    print(f'======================================\n')
    
    # Auto-open browser
    try:
        webbrowser.open(picker_uri)
        logger.info('Opened picker URL in browser.')
    except Exception:
        logger.warning('Could not auto-open browser. Please open the URL manually.')
    
    # Poll for completion
    completed = poll_session(creds, session_id, timeout_seconds=180 if not test else 30)
    
    if not completed:
        delete_session(creds, session_id)
        raise TimeoutError('User did not complete photo selection in time.')
    
    # Fetch selected items
    items = list_media_items(creds, session_id)
    delete_session(creds, session_id)
    
    if limit:
        items = items[:limit]
    
    # Normalize to same format as collector_local.py for pipeline compatibility
    normalized = []
    for item in items:
        md = item.get('mediaMetadata', {})
        normalized.append({
            'id': item.get('id'),
            'filename': item.get('filename'),
            'local_path': None,  # no local path for Picker API items
            'base_url': item.get('baseUrl'),  # temporary download URL (expires)
            'mime_type': item.get('mimeType'),
            'created_time': md.get('creationTime'),
            'width': md.get('width'),
            'height': md.get('height'),
            'source': 'picker_api',
        })
    
    return normalized


def main():
    parser = argparse.ArgumentParser(description='Google Photos Picker API collector (Plan A)')
    parser.add_argument('--test', action='store_true', help='Test mode: pick up to 5 photos')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of items')
    args = parser.parse_args()
    
    items = run_picker_flow(test=args.test, limit=5 if args.test else args.limit)
    
    print(f'\n=== Plan A (Picker API) Results ===')
    print(f'Fetched: {len(items)} items')
    for item in items[:5]:
        print(f'  - {item["filename"]} ({item["mime_type"]})')
    
    if args.test:
        print('\n=> Plan A collector is working correctly.' if items else '\n=> No items selected.')
    
    return items


if __name__ == '__main__':
    main()
