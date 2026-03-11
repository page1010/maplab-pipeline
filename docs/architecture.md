# System Architecture — MAPLAB Digital Asset Pipeline v2.0

---

## Data Flow (Detailed)

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT SOURCES                         │
│  [Google Photos - Owner]  [Google Photos - Spouse]      │
└──────────────────┬──────────────────────────────────────┘
                   │ (incremental fetch, dedup by photo ID)
                   ▼
┌─────────────────────────────────────────────────────────┐
│              MODULE 1: COLLECTOR                         │
│  • Fetch new photos since last run                       │
│  • Download to local temp dir                           │
│  • Extract: photo_id, timestamp, original_filename      │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌────────────────────┐
│  MODULE 2A:   │    │    MODULE 2B:       │
│  EXIF Parser  │    │   CROSS-REFERENCE  │
│               │    │                    │
│ • Pillow      │    │ Sheets: find quote │
│ • GPS→location│    │   by date ±1 day   │
│ • datetime    │    │                    │
│               │    │ Calendar/Gmail:     │
│               │    │   find trip by     │
│               │    │   date range       │
└──────┬────────┘    └────────┬───────────┘
       │                      │
       └──────────┬───────────┘
                  │ Merged: {location, project_name, date}
                  ▼
┌─────────────────────────────────────────────────────────┐
│              MODULE 3: VISION (Gemini)                   │
│  • Send thumbnail to Gemini 1.5 Flash                   │
│  • Input context: location + project_name               │
│  • Output: {category, keywords[3], description}         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              MODULE 4: TRANSFORMER                       │
│  • Convert to WebP (quality=80, max_width=2000px)       │
│  • Filename: {YYYYMMDD}_{Project_Name}_{kw1-kw2-kw3}   │
│  • Write Alt text to metadata                           │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌────────────────────┐
│  MODULE 5A:   │    │    MODULE 5B:       │
│  Google Drive │    │    Notion Log       │
│               │    │                    │
│ Auto-create:  │    │ Create DB entry:   │
│ /MAPLAB_Assets│    │ • Date             │
│ /2026         │    │ • Category         │
│ /03_Catering  │    │ • Project Name     │
│               │    │ • Drive Link       │
│ Upload file   │    │ • AI Keywords      │
│ → get URL     │    │ • Status: 待寫作   │
└───────────────┘    └────────────────────┘
```

---

## Module Specifications

### Module 1: Collector (`src/collector.py`)

**Inputs:** OAuth token, last_processed_timestamp (from state file)  
**Outputs:** List of `PhotoRecord` objects

```python
@dataclass
class PhotoRecord:
    photo_id: str
    original_filename: str
    local_path: str        # temp download path
    captured_at: datetime  # from EXIF or Photos API
    width: int
    height: int
```

**Key logic:**
- Uses `photoslibrary.readonly` scope
- Filters: `dateFilter` with rolling window or incremental
- Dedup: check `processed_ids.json` before downloading
- Handles two accounts via separate token files

---

### Module 2A: EXIF Parser (inside `src/vision.py`)

**Inputs:** `PhotoRecord.local_path`  
**Outputs:** `{gps_lat, gps_lon, location_name, captured_at_confirmed}`

**Key logic:**
- Pillow `Image.getexif()` → ExifTags
- GPS: `geopy.geocoders.Nominatim` → city/district level only
- Fallback: if no EXIF GPS, use Photos API location metadata

---

### Module 2B: Cross-Reference (`src/crossref.py`)

**Inputs:** `captured_at: datetime`  
**Outputs:** `{project_name: str, category: "catering"|"travel"|"other"}`

#### Sheets Logic (Catering)
```
Search MAPLAB_Quotes sheet:
  WHERE date BETWEEN (captured_at - 1day) AND (captured_at + 1day)
  RETURN: client_name, event_theme → compose project_name
```

Column mapping (TBD — confirm with owner):
- Column A: Date
- Column B: Client Name  
- Column C: Event Theme / Menu
- Column D: Quote Amount

#### Calendar/Gmail Logic (Travel)
```
Search Google Calendar:
  WHERE event.start <= captured_at <= event.end
  AND event.description CONTAINS ("旅遊" OR "travel" OR "trip" OR "飛")
  RETURN: event.summary → use as project_name

Fallback - Gmail:
  Search: subject:("航班確認" OR "Flight Confirmation" OR "booking")
  Extract: departure_date, destination
```

**Priority:** Calendar > Sheets > Gmail > "Unknown"

---

### Module 3: Vision (`src/vision.py`)

**Gemini Prompt (v1):**
```
You are a professional SEO content specialist for a premium catering brand in Taiwan.

Analyze this photo. You have this context:
- Capture date: {date}
- Location: {location_name}
- Project context: {project_name} (may be empty)

Return ONLY valid JSON, no markdown:
{
  "category": "catering" | "travel" | "other",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "alt_text": "One sentence description for SEO (English, max 120 chars)",
  "confidence": 0.0-1.0
}

Rules for keywords:
- English only, lowercase, hyphen-separated if compound
- For catering: food items, cooking technique, Taiwanese cuisine
- For travel: location, activity, cultural element
- Make keywords internationally searchable
```

---

### Module 4: Transformer (`src/transformer.py`)

**Filename pattern:**
```python
filename = f"{date_str}_{project_name_slug}_{'-'.join(keywords)}.webp"
# Example: 20260310_tainan-catering-wedding_milkfish-panfry-taiwanese.webp
```

**Slug rules:**
- Lowercase
- Replace spaces and special chars with `-`
- Max 30 chars for project_name_slug
- Max 60 chars total filename (before .webp)

**WebP settings:**
- Quality: 80
- Max width: 2000px (maintain aspect ratio)
- Strip personal EXIF (GPS, author) before export

---

### Module 5A: Drive Archiver (`src/archiver.py`)

**Folder structure:**
```
MAPLAB_Assets/
└── 2026/
    ├── 03_Catering/
    │   └── 20260310_tainan-catering-wedding_milkfish-panfry.webp
    └── 02_Travel/
        └── 20260215_bali-family-trip_temple-ceremony-balinese.webp
```

---

### Module 5B: Notion Logger (`src/archiver.py`)

**Database schema:**

| Property | Type | Notes |
|----------|------|-------|
| Title | Title | Filename (without extension) |
| Date | Date | EXIF capture date |
| Category | Select | catering / travel / other |
| Project Name | Rich Text | From Sheets/Calendar |
| Drive Link | URL | Google Drive file URL |
| AI Keywords | Multi-select | 3 keywords from Gemini |
| Alt Text | Rich Text | SEO description |
| Status | Select | 待寫作 / 已使用 / 已發佈 |
| Original Filename | Rich Text | For traceability |

---

## Error Handling Strategy

| Error | Action |
|-------|--------|
| No EXIF GPS | Use Photos API location; if missing, use "unknown-location" |
| Gemini API failure | Retry 3x with backoff; fallback to filename-based keywords |
| No Sheets match (±1 day) | Try ±3 days; if still no match, category = "other" |
| Drive upload failure | Save to local queue file, retry next run |
| Notion write failure | Log to `failed_notion.jsonl` for manual recovery |

---

## State Persistence

The pipeline maintains `state/pipeline_state.json`:
```json
{
  "last_run": "2026-03-10T14:30:00Z",
  "processed_ids": ["photo_id_1", "photo_id_2"],
  "failed_ids": [],
  "stats": {
    "total_processed": 47,
    "catering": 23,
    "travel": 19,
    "other": 5
  }
}
```

---

*Architecture v2.0 — initialized 2026-03-10 by Claude*
