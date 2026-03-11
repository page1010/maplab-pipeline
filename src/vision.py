"""
Vision Module
1. Extracts EXIF metadata (GPS, timestamp) using Pillow
2. Converts GPS to human-readable location using Geopy
3. Sends photo to Gemini 1.5 Flash for content classification + SEO keywords

Phase: 2
Status: SKELETON — implement after Phase 1 working

Gemini prompt returns:
{
  "category": "catering" | "travel" | "other",
  "keywords": ["kw1", "kw2", "kw3"],
  "alt_text": "One sentence SEO description",
  "confidence": 0.0-1.0
}
"""

import os
import json
import base64
import logging
from pathlib import Path
from typing import Optional
import google.generativeai as genai
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

logger = logging.getLogger('maplab.vision')

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Geocoder (be respectful — this is a free service)
_geocoder = Nominatim(user_agent="maplab-pipeline/1.0")


# ─── Gemini Prompt ──────────────────────────────────────────────────────────

GEMINI_PROMPT_TEMPLATE = """You are a professional SEO content specialist for MAPLAB Kitchen, 
a premium catering brand in Tainan, Taiwan.

Analyze this photo. Context provided:
- Capture date: {date}
- Location: {location_name}
- Project context: {project_name}

Return ONLY valid JSON (no markdown, no explanation):
{{
  "category": "catering" | "travel" | "other",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "alt_text": "One sentence description for SEO (English, max 120 chars)",
  "confidence": 0.0-1.0
}}

Keyword rules:
- English only, lowercase
- For catering: specific food item, cooking technique, cuisine style
- For travel: specific location name, activity, cultural element
- Make keywords internationally searchable for food tourism
- Examples: "milkfish-panfry", "tainan-street-food", "bali-temple-ceremony"
"""


def extract_exif(image_path: str) -> dict:
    """
    Extract EXIF metadata from image using Pillow.
    
    Returns:
        {
            "gps_lat": float | None,
            "gps_lon": float | None,
            "captured_at": datetime | None,
            "camera_model": str | None
        }
    """
    result = {
        "gps_lat": None,
        "gps_lon": None,
        "captured_at": None,
        "camera_model": None
    }
    
    try:
        img = Image.open(image_path)
        exif_raw = img.getexif()
        
        if not exif_raw:
            logger.debug(f"No EXIF data in {image_path}")
            return result
        
        exif = {}
        for tag_id, value in exif_raw.items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = value
        
        # Camera model
        result["camera_model"] = exif.get("Model")
        
        # GPS data
        gps_info = exif.get("GPSInfo")
        if gps_info:
            gps = {}
            for key, val in gps_info.items():
                gps_tag = GPSTAGS.get(key, key)
                gps[gps_tag] = val
            
            lat = _convert_gps(gps.get("GPSLatitude"), gps.get("GPSLatitudeRef"))
            lon = _convert_gps(gps.get("GPSLongitude"), gps.get("GPSLongitudeRef"))
            
            if lat and lon:
                result["gps_lat"] = lat
                result["gps_lon"] = lon
        
    except Exception as e:
        logger.warning(f"EXIF extraction failed for {image_path}: {e}")
    
    return result


def _convert_gps(coord, ref) -> Optional[float]:
    """Convert GPS DMS format to decimal degrees."""
    if not coord or not ref:
        return None
    try:
        d, m, s = float(coord[0]), float(coord[1]), float(coord[2])
        decimal = d + m / 60 + s / 3600
        if ref in ['S', 'W']:
            decimal = -decimal
        return round(decimal, 6)
    except Exception:
        return None


def gps_to_location(lat: float, lon: float) -> str:
    """
    Convert GPS coordinates to human-readable location string.
    Returns city/district level (not street address — for SEO use).
    
    Example: (22.9971, 120.2169) → "tainan-west-central"
    """
    try:
        location = _geocoder.reverse(f"{lat}, {lon}", language='en', timeout=10)
        if not location:
            return "unknown-location"
        
        addr = location.raw.get("address", {})
        
        # Build location slug: city + district
        parts = []
        
        city = addr.get("city") or addr.get("county") or addr.get("town")
        if city:
            parts.append(city)
        
        district = addr.get("suburb") or addr.get("quarter") or addr.get("neighbourhood")
        if district:
            parts.append(district)
        
        # Also try country for travel photos
        country = addr.get("country")
        if country and country not in ["Taiwan", "中華民國"]:
            parts.append(country)
        
        if parts:
            # Slugify
            combined = '-'.join(parts).lower()
            combined = combined.replace(' ', '-').replace(',', '')
            return combined[:40]
        
        return "unknown-location"
        
    except GeocoderTimedOut:
        logger.warning(f"Geocoder timed out for {lat},{lon}")
        return "unknown-location"
    except Exception as e:
        logger.warning(f"Geocoding failed: {e}")
        return "unknown-location"


def analyze_with_gemini(
    image_path: str,
    date: str,
    location_name: str,
    project_name: str
) -> dict:
    """
    Send photo to Gemini 1.5 Flash for classification and SEO keywords.
    
    Returns:
        {
            "category": str,
            "keywords": list[str],
            "alt_text": str,
            "confidence": float
        }
    """
    fallback = {
        "category": "other",
        "keywords": ["maplab", "tainan", "catering"],
        "alt_text": f"MAPLAB Kitchen photo from {date}",
        "confidence": 0.0
    }
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Load and resize image for API (reduce tokens/cost)
        img = Image.open(image_path)
        img.thumbnail((800, 800))
        
        # Convert to bytes for Gemini
        import io
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        img_bytes = buf.getvalue()
        
        prompt = GEMINI_PROMPT_TEMPLATE.format(
            date=date,
            location_name=location_name,
            project_name=project_name or "unknown"
        )
        
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": img_bytes},
            prompt
        ])
        
        # Parse JSON response
        text = response.text.strip()
        # Strip markdown code fences if present
        text = text.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(text)
        
        # Validate expected fields
        if not all(k in result for k in ["category", "keywords", "alt_text"]):
            logger.warning("Gemini response missing fields, using fallback")
            return fallback
        
        logger.info(
            f"Gemini: {result['category']} | "
            f"keywords: {result['keywords']} | "
            f"confidence: {result.get('confidence', '?')}"
        )
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"Gemini returned invalid JSON: {e}")
        return fallback
    except Exception as e:
        logger.error(f"Gemini API call failed: {e}")
        return fallback


def analyze_photo(photo_record, project_info: dict) -> dict:
    """
    Full vision analysis pipeline for one photo.
    
    Args:
        photo_record: PhotoRecord from collector
        project_info: From crossref module
    
    Returns:
        Updated vision data to merge into photo_record
    """
    # Step 1: Extract EXIF
    exif = extract_exif(photo_record.local_path)
    
    # Step 2: GPS to location
    location_name = "tainan-taiwan"  # default
    if exif["gps_lat"] and exif["gps_lon"]:
        location_name = gps_to_location(exif["gps_lat"], exif["gps_lon"])
        logger.info(f"GPS resolved: {location_name}")
    
    # Step 3: Gemini classification
    date_str = photo_record.captured_at.strftime("%Y-%m-%d")
    vision = analyze_with_gemini(
        image_path=photo_record.local_path,
        date=date_str,
        location_name=location_name,
        project_name=project_info.get("project_name", "")
    )
    
    return {
        "gps_lat": exif["gps_lat"],
        "gps_lon": exif["gps_lon"],
        "location_name": location_name,
        "category": vision["category"],
        "keywords": vision["keywords"],
        "alt_text": vision["alt_text"],
        "vision_confidence": vision.get("confidence", 0.0)
    }
