# PROJECT STATE
⚡ AI Collaborator: Read this file FIRST. Update this file LAST.
This is the single source of truth for all AI handoffs.

> **工作規則（給所有 AI 協作者）**：每次工作前先讀此檔案 + 翻閱 Notion 監控面板與 GitHub 各模組 → 完成後更新此檔案 → Token 限制前寫下 Next Task。只跑不需要人工操作的區塊，切割小步驟，每步驟獨立 commit。

---

## 🗓️ Last Updated
- **Date**: 2026-03-11
- **Updated by**: Claude (Sonnet 4.6)
- **Session type**: Block work — checklist update + API Keys vault creation

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
| 1.1 | GCP project created, 5 APIs enabled | Human (owner) | 2026-03-11 |
| 1.2 | credentials.json downloaded, placed in auth/ | Human (owner) | 2026-03-11 |
| 1.3 | Gemini API Key obtained → .env GEMINI_API_KEY filled | Human + AI Studio | 2026-03-11 |
| 2.1 | transformer.py: read WEBP_QUALITY & MAX_IMAGE_WIDTH from .env | Claude | 2026-03-11 |
| 2.2 | pipeline.py: wire all Phase 1-5 modules, remove TODO stubs | Claude | 2026-03-11 |
| 2.3 | tests/test_transformer.py: unit tests for slugify, build_filename, env | Claude | 2026-03-11 |
| 2.4 | Notion checklist: ticked GCP, credentials.json, .env filled | Claude | 2026-03-11 |
| 2.5 | Notion: API Keys 保管室 page created — all keys archived | Claude | 2026-03-11 |
| 2.6 | NOTION_TOKEN obtained from Internal integration | Claude | 2026-03-11 |

---

## 🔄 Current Task
**Phase 1: OAuth 2.0 + Google Photos Collector — READY TO TEST**

- Status: Code complete, all keys filled except NOTION_DATABASE_ID
- What's done: All modules wired, transformer reads .env, NOTION_TOKEN filled
- What's needed to proceed:
  1. Human runs `python src/auth/google_auth.py --account owner`
  2. Human runs `python src/auth/google_auth.py --account spouse`
  3. Human runs `python pipeline.py --test` to verify 1 photo end-to-end
- Blocker: Human action — OAuth browser flow (cannot be automated)

---

## ⏭️ Next Task (for next AI session)
**After OAuth is done by human:**
- Debug if pipeline.py --test fails → check pipeline.log
- NOTION_DATABASE_ID: create a Notion DB for photo assets log, then fill .env

---

## 📋 Full Phase Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffolding | ✅ DONE |
| 1 | OAuth + Collector | 🔄 BLOCKED (human OAuth) |
| 2 | Vision (EXIF+Gemini) | ⏳ PENDING |
| 3 | Cross-reference (Sheets + Calendar) | ⏳ PENDING — Q2 unresolved |
| 4 | WebP Transform | ✅ CODE COMPLETE |
| 5 | Drive + Notion log | ⏳ PENDING — NOTION_DATABASE_ID needed |
| 6 | Integration test | ⏳ PENDING |

---

## ❓ Open Questions

| # | Question | Priority | Notes |
|---|----------|----------|-------|
| Q1 | Google account type: Personal or Workspace? | HIGH | Affects OAuth consent complexity |
| Q2 | MAPLAB_Quotes sheet — exact column names? Date format (YYYY/MM/DD or MM/DD?)? | HIGH | Needed for Phase 3 crossref.py |
| Q3 | NOTION_DATABASE_ID — which DB to use for photo asset log? | HIGH | Need to create or identify existing DB |
| Q4 | Spouse's Google account — same OAuth app or separate credentials? | MEDIUM | Affects collector design |

---

## 🧠 Context for Next AI

**Current .env status:**
- MAPLAB_QUOTES_SHEET_ID: ✅ 1d2_SiEXh5JT4lzjkgHDI5JU9UWBY9TiPlC8DaxkQnKs
- GOOGLE_DRIVE_ARCHIVE_FOLDER_ID: ✅ 1L0udpuXLy3vEbHmzBbaLqNVDut2FFpCe
- GEMINI_API_KEY: ✅ (see Notion API Keys 保管室)
- NOTION_TOKEN: ✅ (see Notion API Keys 保管室)
- NOTION_DATABASE_ID: ❌ still needs to be created/identified

**Notion API Keys 保管室:** https://www.notion.so/API-Keys-maplab-pipeline-320ab0806d5c80e0be95f298399d2c44

**Code status:**
- pipeline.py: fully wired (all phases)
- transformer.py: reads .env for quality/width settings ✅
- collector.py: complete skeleton, needs credentials.json + OAuth
- vision.py: complete, Gemini 1.5 Flash, GPS→location, EXIF
- crossref.py: complete skeleton, Q2 column mapping TBD
- archiver.py: complete skeleton, needs NOTION_DATABASE_ID

---

## 📁 Repository File Map

```
maplab-pipeline/
├── README.md               ← Project overview
├── project_state.md        ← YOU ARE HERE
├── .env.example            ← Credential template
├── requirements.txt        ← Python dependencies
├── src/
│   ├── auth/
│   │   └── google_auth.py  ← OAuth2 flow (Phase 1) — needs credentials.json
│   ├── collector.py        ← Google Photos fetch (Phase 1)
│   ├── vision.py           ← EXIF + Gemini Vision (Phase 2)
│   ├── crossref.py         ← Sheets + Calendar lookup (Phase 3) — Q2 TBD
│   ├── transformer.py      ← WebP conversion (Phase 4) ✅ reads .env
│   ├── archiver.py         ← Drive upload + Notion log (Phase 5)
│   └── pipeline.py         ← Main orchestrator ✅ all modules wired
├── docs/
│   └── naming_rules.md     ← v1.2 (EVT / foodphoto / SEO / AD patterns)
├── schemas/
│   ├── notion_entry.schema.json
│   └── photo_record.schema.json
└── tests/
    ├── test_date_tolerance.py  ← ±1 day matching logic ✅
    └── test_transformer.py     ← slugify + build_filename ✅
```

Always update this file at the end of your session.
