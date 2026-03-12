# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.

> NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.

---

## Last Updated
- Date: 2026-03-12
- Updated by: Claude (Sonnet 4.6)
- Session: Block 3.5 - collector.py SyntaxError fixed, handoff

---

## Project Goal
MAPLAB photos -> WebP SEO assets, cross-referenced with quotes/itineraries, logged to Notion. Original photos never deleted.

---

## Completed Tasks
| # | Task | By | Date |
|---|------|----|------|
| 0.1 | Project scaffolding | Claude | 2026-03-10 |
| 0.2 | AI handoff guide | Claude | 2026-03-10 |
| 0.3 | Python src skeleton | Claude | 2026-03-10 |
| 0.4 | .env.example + requirements.txt | Claude | 2026-03-10 |
| 0.5 | JSON schemas | Claude | 2026-03-10 |
| 1.1 | GCP project, 5 APIs enabled | Human | 2026-03-11 |
| 1.2 | credentials.json placed in auth/ | Human | 2026-03-11 |
| 1.3 | Gemini API Key -> .env | Human | 2026-03-11 |
| 2.1 | transformer.py reads .env | Claude | 2026-03-11 |
| 2.2 | pipeline.py wired Phase 1-5 | Claude | 2026-03-11 |
| 2.3 | test_transformer.py 14 tests | Claude | 2026-03-11 |
| 2.4-2.9 | Notion setup + API keys + ASSET_LOG | Claude | 2026-03-12 |
| 3.1 | OAuth owner confirmed | Human | 2026-03-12 |
| 3.2 | pip install complete | Human | 2026-03-12 |
| 3.3 | pipeline.py Phase 1 uncommented | Claude | 2026-03-12 |
| 3.4 | collector.py owner-only default 30d | Claude | 2026-03-12 |
| 3.5 | collector.py SyntaxError em-dash fixed | Claude | 2026-03-12 |

---

## CURRENT BLOCKER - Human Action Required

403 Forbidden from Google Photos API is NOT fixed.
Root cause: token_owner.json created BEFORE photoslibrary.readonly scope was added.
Old token has no Photos permission.

### Human must do 3 steps:

Step 1 - Pull latest code:
    git pull origin main
    (if conflict: git checkout --theirs README.md && git add README.md && git commit -m fix && git pull origin main)

Step 2 - Re-authorize OAuth:
    del auth\token_owner.json
    python -m src.auth.google_auth --account owner
    Browser opens -> select account -> CONFIRM Google Photos in permissions -> Allow

Step 3 - Verify:
    python -m src.collector --test --account owner
    Expected: [owner] API returned N items -> Fetched 1 photos

---

## Next AI Task (after human does above)
1. Read this file + Notion
2. Human pastes collector test output
3. If 1 photo fetched: mark Phase 1 DONE, tick Notion checklist
4. Run: python src/pipeline.py --test
5. Implement Phase 2: vision.py EXIF + Gemini

---

## SAFETY RULES
1. NEVER delete original photos
2. NEVER commit .env
3. NEVER share API Keys page URL

---

## Phase Roadmap
| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffolding | DONE |
| 1 | OAuth + Collector | BLOCKED - need re-auth to fix 403 |
| 2 | Vision EXIF+Gemini | PENDING |
| 3 | Cross-reference Sheets | PENDING Q2 unresolved |
| 4 | WebP Transform | CODE DONE |
| 5 | Drive + Notion log | NOTION_DATABASE_ID ready |
| 6 | Integration test | PENDING |

---

## Open Questions
| # | Question | Priority |
|---|----------|----------|
| Q1 | Google account Personal or Workspace? | HIGH |
| Q2 | MAPLAB_Quotes sheet column names + date format? | HIGH |
| Q3 | Spouse OAuth done? token_spouse.json exist? | MEDIUM |
| Q4 | Spouse same OAuth app or separate? | MEDIUM |

---

## Key Config
.env (all filled):
- MAPLAB_QUOTES_SHEET_ID: 1d2_SiEXh5JT4lzjkgHDI5JU9UWBY9TiPlC8DaxkQnKs
- GOOGLE_DRIVE_ARCHIVE_FOLDER_ID: 1L0udpuXLy3vEbHmzBbaLqNVDut2FFpCe
- GEMINI_API_KEY: see Notion API Keys page
- NOTION_TOKEN: see Notion API Keys page
- NOTION_DATABASE_ID: 320ab0806d5c801b9063d444cd7fbd1c

Auth:
- token_owner.json: EXISTS but wrong scope -> needs re-auth
- token_spouse.json: not confirmed

ASSET_LOG DB: https://www.notion.so/320ab0806d5c801b9063d444cd7fbd1c
Columns: Name, Date, Category, Project Name, Drive Link, AI Keywords, Alt Text, Status, Original Filename, Output Size KB

Code status:
- pipeline.py: Phase 1 live
- collector.py: FIXED SyntaxError + owner-only + timezone.utc
- transformer.py: reads .env
- vision.py: skeleton Phase 2 TODO
- crossref.py: skeleton Q2 TBD
- archiver.py: skeleton NOTION_DATABASE_ID ready

Always update this file at the end of your session.
