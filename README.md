# MAPLAB 數位資產自動化工作流 v2.0

> **This is an AI-Collaborative Project.**  
> If you are an AI assistant (Claude / GPT / Gemini), **start here → read `project_state.md` first**.

---

## 🧭 Quick Navigation for AI Collaborators

| File | Purpose |
|------|---------|
| [`project_state.md`](./project_state.md) | **Current status, active task, next task** — read this first every session |
| [`docs/architecture.md`](./docs/architecture.md) | System design, module breakdown, data flow |
| [`docs/ai_handoff_guide.md`](./docs/ai_handoff_guide.md) | How to write proper handoffs between AI sessions |
| [`docs/api_context.md`](./docs/api_context.md) | API credentials scope, expected data shapes |
| [`src/`](./src/) | Python source code |
| [`schemas/`](./schemas/) | Data contracts (JSON schemas for Notion, Sheets, etc.) |

---

## 🎯 Project Goal

Build a Python automation pipeline that:

1. **Collects** photos from Google Photos (two accounts: owner + spouse)
2. **Extracts** EXIF metadata (time, GPS → human-readable location)
3. **Classifies** content via Gemini Vision (Catering vs Travel, SEO keywords)
4. **Cross-references** with Google Sheets (MAPLAB catering quotes) and Google Calendar / Gmail (travel itineraries)
5. **Transforms** files to WebP (2000px wide, quality 80)
6. **Renames** using pattern: `{YYYYMMDD}_{Project_Name}_{keywords}.webp`
7. **Archives** to Google Drive structured folders
8. **Logs** everything to Notion database (writing materials dashboard)

---

## 🏗️ System Architecture (Overview)

```
[Google Photos API] ──► [Collector Module]
                                │
                    ┌───────────┴────────────┐
          [Sheets API]              [Calendar/Gmail API]
          Quote Lookup              Trip Lookup
                    └───────────┬────────────┘
                                │ Project_Name resolved
                         [Vision Module]
                         Gemini 1.5 Flash
                         EXIF + AI Keywords
                                │
                        [Transform Module]
                        Pillow: JPG/HEIC → WebP
                                │
                   ┌────────────┴───────────┐
           [Drive API]              [Notion API]
           Archive files            Log dashboard entry
```

---

## 📦 Tech Stack

- **Language:** Python 3.11+
- **Core APIs:** Google Photos, Google Sheets, Google Calendar, Gmail, Google Drive, Notion
- **AI Vision:** Gemini 1.5 Flash
- **Image Processing:** Pillow, img2webp
- **Auth:** OAuth 2.0 (Google), Notion Integration Token

---

## 🚦 Current Phase

See [`project_state.md`](./project_state.md) for live status.

**Phase Overview:**
- [x] Phase 0: Project scaffolding & documentation
- [ ] Phase 1: OAuth + Google Photos collector (skeleton)
- [ ] Phase 2: EXIF extraction + Gemini Vision classification
- [ ] Phase 3: Sheets + Calendar cross-reference (±1 day tolerance)
- [ ] Phase 4: WebP transform + SEO renaming
- [ ] Phase 5: Drive archive + Notion logging
- [ ] Phase 6: End-to-end integration test

---

## 🔑 Environment Setup

Copy `.env.example` to `.env` and fill in credentials:

```bash
cp .env.example .env
```

Required environment variables:
```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
NOTION_TOKEN=
NOTION_DATABASE_ID=
GEMINI_API_KEY=
MAPLAB_QUOTES_SHEET_ID=
GOOGLE_DRIVE_ARCHIVE_FOLDER_ID=
```

---

## ⚠️ Key Design Decisions

1. **Date tolerance ±1 day** when matching photos to catering quotes (prep photos taken day before event)
2. **Incremental processing** — track processed photo IDs to avoid re-processing
3. **Two Google accounts** — owner + spouse share photos; need dual OAuth tokens
4. **Gemini prompt language** — English keywords for SEO (international discoverability)

---

*Project owner: MAPLAB Kitchen, Tainan, Taiwan*  
*Last updated: see `project_state.md`*
