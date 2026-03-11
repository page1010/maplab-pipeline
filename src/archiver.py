"""
Archiver Module
1. Uploads transformed WebP to Google Drive (auto-creates folder structure)
2. Logs entry to Notion database

Phase: 5
Status: SKELETON

Drive folder structure:
    MAPLAB_Assets/
    └── 2026/
        ├── 03_Catering/
        └── 02_Travel/
        
Notion DB properties:
    Title, Date, Category, Project Name, Drive Link,
    AI Keywords, Alt Text, Status, Original Filename
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from notion_client import Client as NotionClient

from src.auth.google_auth import authenticate

logger = logging.getLogger('maplab.archiver')

DRIVE_ROOT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_ARCHIVE_FOLDER_ID")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID")

# Category to month prefix mapping
CATEGORY_FOLDER = {
    "catering": "Catering",
    "travel": "Travel",
    "other": "Misc"
}


def _get_or_create_folder(service, name: str, parent_id: str) -> str:
    """
    Get existing Drive folder by name under parent, or create it.
    Returns folder ID.
    """
    query = (
        f"name='{name}' and "
        f"'{parent_id}' in parents and "
        f"mimeType='application/vnd.google-apps.folder' and "
        f"trashed=false"
    )
    
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    
    if files:
        return files[0]["id"]
    
    # Create folder
    folder_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    logger.info(f"Created Drive folder: {name}")
    return folder["id"]


def archive_to_drive(
    output_path: str,
    filename: str,
    captured_at: datetime,
    category: str
) -> str:
    """
    Upload WebP file to Google Drive in structured folder.
    
    Returns:
        Google Drive file URL (shareable link)
    """
    creds = authenticate('owner')
    service = build('drive', 'v3', credentials=creds)
    
    # Build folder path: root / year / category
    year_str = captured_at.strftime("%Y")
    cat_folder_name = CATEGORY_FOLDER.get(category, "Misc")
    
    year_folder_id = _get_or_create_folder(service, year_str, DRIVE_ROOT_FOLDER_ID)
    cat_folder_id = _get_or_create_folder(service, cat_folder_name, year_folder_id)
    
    # Upload file
    file_metadata = {
        "name": filename,
        "parents": [cat_folder_id]
    }
    
    media = MediaFileUpload(output_path, mimetype="image/webp", resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink"
    ).execute()
    
    drive_url = file.get("webViewLink", "")
    logger.info(f"Uploaded to Drive: {filename} → {drive_url}")
    
    # Clean up local file after successful upload
    Path(output_path).unlink(missing_ok=True)
    
    return drive_url


def log_to_notion(
    photo_record,
    project_info: dict,
    vision_result: dict,
    transform_result: dict,
    drive_url: str
) -> str:
    """
    Create a new entry in Notion database.
    
    Returns:
        Notion page ID of created entry
    """
    if not NOTION_TOKEN or not NOTION_DB_ID:
        logger.error("Notion credentials not configured in .env")
        raise ValueError("NOTION_TOKEN and NOTION_DATABASE_ID required")
    
    notion = NotionClient(auth=NOTION_TOKEN)
    
    filename_stem = transform_result.get("filename", "unknown").replace(".webp", "")
    keywords = vision_result.get("keywords", [])
    
    # Build Notion page properties
    properties = {
        # Title
        "Name": {
            "title": [{"text": {"content": filename_stem}}]
        },
        # Date
        "Date": {
            "date": {
                "start": photo_record.captured_at.strftime("%Y-%m-%d")
            }
        },
        # Category (Select)
        "Category": {
            "select": {
                "name": project_info.get("category", "other").capitalize()
            }
        },
        # Project Name
        "Project Name": {
            "rich_text": [{"text": {"content": project_info.get("project_name", "")}}]
        },
        # Drive Link
        "Drive Link": {
            "url": drive_url
        },
        # AI Keywords (Multi-select)
        "AI Keywords": {
            "multi_select": [{"name": kw} for kw in keywords[:3]]
        },
        # Alt Text
        "Alt Text": {
            "rich_text": [{"text": {"content": vision_result.get("alt_text", "")}}]
        },
        # Status (Select)
        "Status": {
            "select": {"name": "待寫作"}
        },
        # Original Filename
        "Original Filename": {
            "rich_text": [{"text": {"content": photo_record.original_filename}}]
        },
        # File Size
        "Output Size KB": {
            "number": transform_result.get("output_size_kb", 0)
        }
    }
    
    response = notion.pages.create(
        parent={"database_id": NOTION_DB_ID},
        properties=properties
    )
    
    page_id = response.get("id", "")
    logger.info(f"Notion entry created: {filename_stem} → {page_id}")
    
    return page_id


def archive_and_log(
    photo_record,
    project_info: dict,
    vision_result: dict,
    transform_result: dict
) -> dict:
    """
    Full archive + log sequence for one photo.
    Returns summary dict.
    """
    # Step 1: Upload to Drive
    drive_url = archive_to_drive(
        output_path=transform_result["output_path"],
        filename=transform_result["filename"],
        captured_at=photo_record.captured_at,
        category=project_info.get("category", "other")
    )
    
    # Step 2: Log to Notion
    try:
        notion_page_id = log_to_notion(
            photo_record=photo_record,
            project_info=project_info,
            vision_result=vision_result,
            transform_result=transform_result,
            drive_url=drive_url
        )
    except Exception as e:
        # Don't fail the whole pipeline if Notion logging fails
        logger.error(f"Notion logging failed: {e}")
        notion_page_id = None
        
        # Save to recovery file
        import json
        with open("failed_notion.jsonl", "a") as f:
            f.write(json.dumps({
                "filename": transform_result["filename"],
                "drive_url": drive_url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n")
    
    return {
        "drive_url": drive_url,
        "notion_page_id": notion_page_id,
        "filename": transform_result["filename"]
    }
