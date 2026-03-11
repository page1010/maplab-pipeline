"""
Cross-Reference Module
Resolves photo date → project_name by checking:
1. Google Sheets (MAPLAB catering quotes) — with ±1 day tolerance
2. Google Calendar / Gmail (travel itineraries)

Phase: 3
Status: SKELETON — implement after Phase 1 & 2 working

Key design: ±1 day tolerance for catering (prep photos taken day before)
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from googleapiclient.discovery import build

from src.auth.google_auth import authenticate

logger = logging.getLogger('maplab.crossref')

# From .env
QUOTES_SHEET_ID = os.getenv("MAPLAB_QUOTES_SHEET_ID")
QUOTES_SHEET_RANGE = "Sheet1!A:D"  # TODO: confirm actual sheet name & columns

# Keywords that indicate travel events in Calendar
TRAVEL_KEYWORDS = ["旅遊", "travel", "trip", "飛", "flight", "holiday", "vacation", "出發"]


def resolve_project(
    captured_at: datetime,
    date_tolerance_days: int = 1
) -> dict:
    """
    Resolve a photo's capture date to a project name and category.
    
    Priority order:
    1. Google Calendar (travel events)
    2. Google Sheets (catering quotes, with ±tolerance)
    3. Gmail (flight confirmations)
    4. Fallback: {"project_name": "misc", "category": "other"}
    
    Args:
        captured_at: Photo capture datetime
        date_tolerance_days: Days of tolerance for Sheets matching (default: 1)
    
    Returns:
        {
            "project_name": str,
            "category": "catering" | "travel" | "other",
            "source": "calendar" | "sheets" | "gmail" | "fallback",
            "confidence": float
        }
    """
    # Try Calendar first (travel events are date ranges, exact)
    calendar_result = _check_calendar(captured_at)
    if calendar_result:
        return calendar_result
    
    # Try Sheets (catering quotes with date tolerance)
    sheets_result = _check_sheets(captured_at, date_tolerance_days)
    if sheets_result:
        return sheets_result
    
    # Try Gmail (flight confirmations)
    gmail_result = _check_gmail(captured_at)
    if gmail_result:
        return gmail_result
    
    logger.info(f"No project match for {captured_at.date()} — using fallback")
    return {
        "project_name": f"misc_{captured_at.strftime('%Y%m')}",
        "category": "other",
        "source": "fallback",
        "confidence": 0.0
    }


def _check_calendar(captured_at: datetime) -> Optional[dict]:
    """
    Check if photo date falls within a travel event in Google Calendar.
    Returns None if no match found.
    """
    try:
        creds = authenticate('owner')
        service = build('calendar', 'v3', credentials=creds)
        
        # Search a window around capture date
        time_min = (captured_at - timedelta(days=1)).isoformat() + 'Z'
        time_max = (captured_at + timedelta(days=1)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        for event in events:
            summary = event.get('summary', '').lower()
            description = event.get('description', '').lower()
            combined = summary + ' ' + description
            
            if any(kw.lower() in combined for kw in TRAVEL_KEYWORDS):
                project_name = _slugify(event.get('summary', 'travel'))
                logger.info(f"Calendar match: {project_name}")
                return {
                    "project_name": project_name,
                    "category": "travel",
                    "source": "calendar",
                    "confidence": 0.95
                }
        
        return None
        
    except Exception as e:
        logger.warning(f"Calendar lookup failed: {e}")
        return None


def _check_sheets(
    captured_at: datetime,
    tolerance_days: int = 1
) -> Optional[dict]:
    """
    Check Google Sheets for catering quotes matching the photo date ±tolerance.
    Returns None if no match found.
    
    TODO: Confirm exact column mapping with MAPLAB owner.
    Assumed: Col A=Date, Col B=Client, Col C=Theme/Menu, Col D=Amount
    """
    if not QUOTES_SHEET_ID:
        logger.warning("MAPLAB_QUOTES_SHEET_ID not set in .env")
        return None
    
    try:
        creds = authenticate('owner')
        service = build('sheets', 'v4', credentials=creds)
        
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=QUOTES_SHEET_ID,
            range=QUOTES_SHEET_RANGE
        ).execute()
        
        rows = result.get('values', [])
        if not rows:
            return None
        
        target_date = captured_at.date()
        
        for row in rows[1:]:  # Skip header row
            if len(row) < 2:
                continue
            
            # Parse date from sheet (handle multiple formats)
            row_date = _parse_date_flexible(row[0])
            if row_date is None:
                continue
            
            # Check ±tolerance window
            delta = abs((target_date - row_date).days)
            if delta <= tolerance_days:
                client_name = row[1] if len(row) > 1 else "client"
                event_theme = row[2] if len(row) > 2 else ""
                
                # Compose project name: combine client + theme
                parts = [p for p in [client_name, event_theme] if p]
                project_name = _slugify('-'.join(parts[:2]))
                
                logger.info(
                    f"Sheets match (±{delta}d): {project_name} "
                    f"| row date: {row_date} | photo: {target_date}"
                )
                return {
                    "project_name": project_name,
                    "category": "catering",
                    "source": "sheets",
                    "confidence": 1.0 if delta == 0 else 0.8
                }
        
        return None
        
    except Exception as e:
        logger.warning(f"Sheets lookup failed: {e}")
        return None


def _check_gmail(captured_at: datetime) -> Optional[dict]:
    """
    Search Gmail for flight confirmations near the photo date.
    Returns None if no match found.
    
    TODO: Parse flight destination from email body.
    """
    try:
        creds = authenticate('owner')
        service = build('gmail', 'v1', credentials=creds)
        
        # Search for flight emails around that date
        date_str = captured_at.strftime('%Y/%m/%d')
        query = (
            f'(subject:"航班確認" OR subject:"Flight Confirmation" OR '
            f'subject:"booking confirmation") '
            f'after:{captured_at.strftime("%Y/%m/%d")}'
        )
        
        result = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=5
        ).execute()
        
        messages = result.get('messages', [])
        
        if messages:
            # TODO: Parse destination from email body
            # For now, return generic travel match
            logger.info("Gmail flight confirmation found near photo date")
            return {
                "project_name": f"travel_{captured_at.strftime('%Y%m')}",
                "category": "travel",
                "source": "gmail",
                "confidence": 0.7
            }
        
        return None
        
    except Exception as e:
        logger.warning(f"Gmail lookup failed: {e}")
        return None


def _parse_date_flexible(date_str: str):
    """Parse date from various formats used in sheets."""
    formats = [
        "%Y/%m/%d", "%Y-%m-%d", "%m/%d/%Y",
        "%Y年%m月%d日", "%m/%d", "%Y/%m/%d %H:%M"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    logger.warning(f"Could not parse date: '{date_str}'")
    return None


def _slugify(text: str, max_len: int = 30) -> str:
    """Convert text to URL/filename safe slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:max_len].strip('-')
