# PROJECT STATE
> **⚡ AI Collaborator: Read this file FIRST. Update this file LAST.**  
> This is the single source of truth for all AI handoffs.

---

## 🗓️ Last Updated
- **Date:** 2026-03-10
- **Updated by:** Claude (Sonnet 4.6)
- **Session type:** Project initialization

---

## 🎯 Project Goal (One Line)
Build a Python pipeline that auto-processes MAPLAB photos → WebP assets with SEO names, cross-referenced with catering quotes and travel itineraries, logged to Notion.

---

## ✅ Completed Tasks

| # | Task | Completed by | Date |
|---|------|-------------|------|
| 0.1 | Project scaffolding: README, architecture docs, project_state | Claude | 2026-03-10 |
| 0.2 | AI handoff guide created | Claude | 2026-03-10 |
| 0.3 | Python src skeleton (5 modules) | Claude | 2026-03-10 |
| 0.4 | .env.example + requirements.txt | Claude | 2026-03-10 |
| 0.5 | JSON schemas (Notion, Sheets) | Claude | 2026-03-10 |

---

## 🔄 Current Task

**Phase 1: OAuth 2.0 Framework + Google Photos Collector**

Status: `SKELETON WRITTEN — NEEDS CREDENTIALS TO TEST`

What's done:
- `src/auth/google_auth.py` — OAuth2 flow skeleton
- `src/collector.py` — Google Photos API fetch skeleton
- All modules stubbed with `TODO` markers

What's needed to proceed:
1. Owner creates Google Cloud Project → enables 5 APIs (Photos, Sheets, Calendar, Gmail, Drive)
2. Downloads `credentials.json` → places in `./auth/` folder
3. Runs `python src/auth/google_auth.py` to generate `token.json`
4. Runs `python src/collector.py --test` to verify connection

Blocker: **Human action required** — Google Cloud credentials setup

---

## ⏭️ Next Task

**Phase 2: EXIF Extraction + Gemini Vision Classification**

Prerequisites: Phase 1 working (can download at least 1 photo)

What to build:
- `src/vision.py` — read EXIF (Pillow), call Gemini API
- GPS → human location via `geopy` (Nominatim)
- Gemini prompt returns: `{category: "catering"|"travel", keywords: ["kw1","kw2","kw3"]}`

Assigned to: Next AI collaborator

---

## 📋 Full Phase Roadmap

```
Phase 0: Scaffolding          [DONE ✅]
Phase 1: OAuth + Collector    [IN PROGRESS 🔄] → BLOCKED on credentials
Phase 2: Vision (EXIF+Gemini) [PENDING]
Phase 3: Cross-reference      [PENDING] — Sheets quotes + Calendar trips
Phase 4: WebP Transform       [PENDING]
Phase 5: Drive + Notion log   [PENDING]
Phase 6: Integration test     [PENDING]
```

---

## ❓ Open Questions

| # | Question | Priority | Notes |
|---|---------|---------|-------|
| Q1 | Google Photos API still requires OAuth consent screen verification for external users — is owner's Google account Personal or Workspace? | HIGH | Affects OAuth setup complexity |
| Q2 | MAPLAB_Quotes sheet — what are the exact column names? Date format (YYYY/MM/DD or MM/DD?)? | HIGH | Needed for Phase 3 |
| Q3 | Notion database ID for the asset log — is there an existing DB or create new? | MEDIUM | Tokens currently exhausted |
| Q4 | Spouse's Google account — will she authorize via the same OAuth app, or separate credentials? | MEDIUM | Affects collector design |
| Q5 | Drive folder structure — existing or let pipeline auto-create? | LOW | Default: pipeline creates |

---

## 🧠 Context for Next AI

**If you are continuing Phase 1 (testing OAuth):**
- Check `src/auth/google_auth.py` — the OAuth flow is written but untested
- The user needs a `credentials.json` from Google Cloud Console
- Scopes required: `photoslibrary.readonly`, `spreadsheets.readonly`, `calendar.readonly`, `gmail.readonly`, `drive.file`

**If you are starting Phase 2 (Vision):**
- Phase 1 must be working first
- Gemini API key goes in `.env` as `GEMINI_API_KEY`
- Target model: `gemini-1.5-flash` (cost-efficient)
- Prompt template is in `docs/prompts.md`

**Design constraint to remember:**
- Date matching uses ±1 day tolerance (prep photos taken day before catering event)
- File naming pattern: `{YYYYMMDD}_{Project_Name}_{kw1}-{kw2}-{kw3}.webp`

---

## 📁 Repository File Map

```
maplab-pipeline/
├── README.md                    ← Project overview
├── project_state.md             ← YOU ARE HERE
├── .env.example                 ← Credential template
├── requirements.txt             ← Python dependencies
├── src/
│   ├── auth/
│   │   └── google_auth.py       ← OAuth2 flow (Phase 1)
│   ├── collector.py             ← Google Photos fetch (Phase 1)
│   ├── vision.py                ← EXIF + Gemini Vision (Phase 2)
│   ├── crossref.py              ← Sheets + Calendar lookup (Phase 3)
│   ├── transformer.py           ← WebP conversion (Phase 4)
│   ├── archiver.py              ← Drive upload + Notion log (Phase 5)
│   └── pipeline.py              ← Main orchestrator (Phase 6)
├── docs/
│   ├── architecture.md          ← Full system design
│   ├── ai_handoff_guide.md      ← How to do handoffs
│   ├── api_context.md           ← API shapes & expectations
│   └── prompts.md               ← Gemini prompt templates
├── schemas/
│   ├── notion_entry.schema.json ← Notion DB entry contract
│   └── photo_record.schema.json ← Internal data shape
└── tests/
    └── test_date_tolerance.py   ← ±1 day matching logic
```

---

*Always update this file at the end of your session.*
