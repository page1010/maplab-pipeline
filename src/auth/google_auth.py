"""
Google OAuth 2.0 Authentication Module
Handles token creation, refresh, and multi-account support.

Phase: 1 (implement this first)
Status: ACTIVE

Setup instructions:
1. Go to https://console.cloud.google.com
2. Create new project -> "MAPLAB Pipeline"
3. Enable APIs: Photos Library, Sheets, Calendar, Gmail, Drive
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials.json -> place in ./auth/ folder
6. Run: python src/auth/google_auth.py --account owner
"""

import os
import json
import logging
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger('maplab.auth')

# All required scopes
SCOPES = [
        'https://www.googleapis.com/auth/photoslibrary.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/drive.file',
]

AUTH_DIR = Path('./auth')
CREDENTIALS_FILE = AUTH_DIR / 'credentials.json'


def get_token_path(account: str) -> Path:
        """Returns token file path for a given account (owner or spouse)."""
        return AUTH_DIR / f'token_{account}.json'


def authenticate(account: str = 'owner') -> Credentials:
        """
            Authenticate and return valid Google credentials.

                Args:
                        account: 'owner' or 'spouse' -- each has separate token file

                            Returns:
                                    Valid Google OAuth2 Credentials object

                                        Raises:
                                                FileNotFoundError: If credentials.json not found
                                                        Exception: If OAuth flow fails
                                                            """
        token_path = get_token_path(account)
        creds = None

    # Load existing token if available
        if token_path.exists():
                    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
                    logger.info(f"Loaded existing token for {account}")

        # Refresh or create new token
        if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                                    logger.info(f"Refreshing expired token for {account}")
                                    creds.refresh(Request())
        else:
                        if not CREDENTIALS_FILE.exists():
                                            raise FileNotFoundError(
                                                                    f"credentials.json not found at {CREDENTIALS_FILE}\n"
                                                                    "Download from Google Cloud Console -> OAuth 2.0 Credentials"
                                            )
                                        logger.info(f"Starting OAuth flow for {account}...")
                        flow = InstalledAppFlow.from_client_secrets_file(
                            str(CREDENTIALS_FILE),
                            SCOPES
                        )
                        # prompt='consent' forces Google to show the consent screen every time
                        # This ensures photoslibrary.readonly (sensitive scope) is actually granted
                        # Without this, Google reuses old token from cache - silently missing new scopes
                        creds = flow.run_local_server(port=0, prompt='consent')
                        logger.info(f"OAuth flow complete for {account}")

            # Save token for next run
                    AUTH_DIR.mkdir(exist_ok=True)
        with open(token_path, 'w') as f:
                        f.write(creds.to_json())
                    logger.info(f"Token saved: {token_path}")

    return creds


def verify_credentials(account: str = 'owner') -> bool:
        """Quick check if credentials are valid without triggering OAuth flow."""
    token_path = get_token_path(account)
    if not token_path.exists():
                return False
            try:
                        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
                        return creds.valid or (creds.expired and creds.refresh_token is not None)
except Exception:
        return False


if __name__ == '__main__':
        import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--account', choices=['owner', 'spouse'], default='owner')
    args = parser.parse_args()

    print(f"Authenticating account: {args.account}")
    creds = authenticate(args.account)
    print(f"Authentication successful for {args.account}")
    print(f"  Token valid: {creds.valid}")
    print(f"  Token expiry: {creds.expiry}")
