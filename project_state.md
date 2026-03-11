# PROJECT STATE
⚡ AI Collaborator: Read this file FIRST. Update this file LAST.
This is the single source of truth for all AI handoffs.

> **工作規則（給所有 AI 協作者）**：每次工作前先讀此檔案 + 翻閱 Notion 監控面板與 GitHub 各模組 → 完成後更新此檔案 → Token 限制前寫下 Next Task。只跑不需要人工操作的區塊，切割小步驟，每步驟獨立 commit。

---

## 🗓️ Last Updated
- **Date**: 2026-03-11
- **Updated by**: Claude (Sonnet 4.6)
- **Session type**: Block work — no-human-required tasks

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

---

## 🔄 Current Task
**Phase 1: OAuth 2.0 + Google Photos Collector — READY TO TEST**

- Status: Code complete, waiting for human to run OAuth flow
- What's done: All modules wired in pipeline.py, transformer reads .env
- What's needed to proceed:
  1. Human runs `python src/auth/google_auth.py --account owner` → browser OAuth popup
  2. Human runs `python src/auth/google_auth.py --account spouse` → second OAuth
  3. Human runs `python pipeline.py --test` → verify 1 photo end-to-end
- Blocker: Human action — OAuth browser flow (cannot be automated)

---

## ⏭️ Next Task (for next AI session)
**After OAuth is done by human:**

Phase 1 test debugging — if `python pipeline.py --test` fails:
- Check pipeline.log for which phase failed
- Common issues: scope mismatch in google_auth.py, QUOTES_SHEET_RANGE wrong column
- Fix and re-run

**After pipeline.py --test passes:**
- Update this file: mark Phase 1 ✅
- Assign: Next AI → Phase 2 vision.py prompt tuning (Gemini prompt template optimization)

---

## 📋 Full Phase Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffolding | ✅ DONE |
| 1 | OAuth + Collector | 🔄 BLOCKED (human OAuth) |
| 2 | Vision (EXIF+Gemini) | ⏳ PENDING |
| 3 | Cross-reference (Sheets + Calendar) | ⏳ PENDING — Q2 unresolved |
| 4 | WebP Transform | ✅ CODE COMPLETE (needs integration test) |
| 5 | Drive + Notion log | ⏳ PENDING — needs NOTION_TOKEN |
| 6 | Integration test | ⏳ PENDING |

---

## ❓ Open Questions

| # | Question | Priority | Notes |
|---|----------|----------|-------|
| Q1 | Google account type: Personal or Workspace? | HIGH | Affects OAuth consent complexity |
| Q2 | MAPLAB_Quotes sheet — exact column names? Date format (YYYY/MM/DD or MM/DD?)? | HIGH | Needed for Phase 3 crossref.py |
| Q3 | Notion database ID for asset log — existing DB or create new? | HIGH | NOTION_DATABASE_ID still placeholder in .env |
| Q4 | NOTION_TOKEN — obtained? | HIGH | Still secret_your_token_here in .env |
| Q5 | Spouse's Google account — same OAuth app or separate credentials? | MEDIUM | Affects collector design |
| Q6 | Drive folder structure — existing or let pipeline auto-create? | LOW | Default: pipeline creates |

---

## 🧠 Context for Next AI

**Current .env status:**
- MAPLAB_QUOTES_SHEET_ID: ✅ filled
- GOOGLE_DRIVE_ARCHIVE_FOLDER_ID: ✅ filled
- GEMINI_API_KEY: ✅ filled (2026-03-11)
- NOTION_TOKEN: ❌ still placeholder
- NOTION_DATABASE_ID: ❌ still placeholder

**Code status:**
- pipeline.py: fully wired (all phases)
- transformer.py: reads .env for quality/width settings
- collector.py: complete skeleton, needs credentials.json to test
- vision.py: complete, Gemini 1.5 Flash, GPS→location, EXIF
- crossref.py: complete skeleton, Q2 column mapping TBD
- archiver.py: complete skeleton, needs NOTION_TOKEN

**Test to run first:**
```
python -m pytest tests/ -v
python pipeline.py --test
```

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
│   ├── architecture.md
│   ├── ai_handoff_guide.md
│   ├── api_context.md
│   ├── prompts.md
│   └── naming_rules.md     ← v1.2 (EVT / foodphoto / SEO / AD patterns)
├── schemas/
│   ├── notion_entry.schema.json
│   └── photo_record.schema.json
└── tests/
    ├── test_date_tolerance.py  ← ±1 day matching logic ✅
    └── test_transformer.py     ← slugify + build_filename ✅ (added 2026-03-11)
```

---

## 🏷️ Naming Rules
See docs/naming_rules.md (v1.2, 2026-03-11) for full image naming patterns (EVT / foodphoto / SEO / AD).

Always update this file at the end of your session.
