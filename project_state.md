# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.
>
> > NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.

---

## Last Updated
- Date: 2026-03-14
- Updated by: Claude (Sonnet 4.6) — A4 Pipeline Agent
- Session: OAuth 500 error diagnosis. GCP app = Production. google_auth.py reduced to photos-only scope (PR #2 merged). Local files still need git pull.

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
| 3.6 | google_auth.py prompt=consent fix (Gemini diagnosis) | Claude | 2026-03-12 |
| 3.7 | New OAuth client + credentials.json re-downloaded | Human | 2026-03-13 |
| 3.8 | auth/setup_credentials.py added (auto-copy from Downloads) | Claude | 2026-03-13 |
| 3.9 | git pull --no-edit success | Human | 2026-03-13 |
| 3.10 | NEVER edit .py via GitHub web UI (IndentationError documented) | Claude | 2026-03-13 |
| 3.11 | PR #1: Fix corrupted google_auth.py + setup_credentials.py via GitHub API | Claude | 2026-03-14 |
| 3.12 | GCP photoslibrary.readonly added to OAuth consent scopes | Claude | 2026-03-14 |
| 3.13 | GCP app status changed from Testing to Production | Claude | 2026-03-14 |
| 3.14 | PR #2: Reduce SCOPES to photos-only for OAuth 500 diagnosis (Gemini diagnosis) | Claude | 2026-03-14 |

---

## CURRENT BLOCKER — OAuth 500 Internal Server Error

**Status**: google_auth.py now has photos-only scope (PR #2 merged). Need local git pull + re-auth test.

**Root cause hypothesis (Gemini)**: Multiple Restricted Scopes (gmail + calendar + sheets + photoslibrary) simultaneously triggers OAuth 500. photoslibrary alone should succeed.

### IMMEDIATE FIX (run these commands):
```bash
git fetch origin
git checkout origin/main -- src/auth/google_auth.py
del auth\token_owner.json
python -m src.auth.google_auth --account owner
python -m src.collector --test --account owner
```
Expected: Fetched > 0 photos

If OAuth still 500 after photos-only scope:
- Delete OAuth client in GCP, create new one, re-download credentials.json
- Check if another process is using the localhost port

---

## Error Log
| ID | Error | Root Cause | Fix | Date |
|----|-------|-----------|-----|------|
| error-001 | Fetched 0 photos (collector) | token.json had no photos scope (old cached token) | del token + prompt=consent re-auth | 2026-03-12 |
| error-002 | 403 PERMISSION_DENIED | photoslibrary.readonly not registered in GCP OAuth consent screen | Added scope in GCP Auth Platform > 資料存取權 | 2026-03-13 |
| error-003 | IndentationError line 78 (google_auth.py) | GitHub web UI editor corrupts Python indentation on commit | NEVER use GitHub web editor for .py files. Use GitHub API via branch+PR. | 2026-03-13 |
| error-004 | OAuth 500 Internal Server Error | GCP app in Testing mode + multiple Restricted Scopes conflict | Changed to Production. Reduced SCOPES to photos-only (PR #2). | 2026-03-14 |

---

## Next AI Task
1. Confirm local git pull completed (git log --oneline -3)
2. del auth\token_owner.json
3. python -m src.auth.google_auth --account owner (should succeed, no 500)
4. python -m src.collector --test --account owner
5. If Fetched > 0: Phase 1 DONE, update this file, start Phase 2: vision.py
6. If still 500: reset GCP OAuth client credentials

---

## SAFETY RULES
1. NEVER delete original photos
2. NEVER commit .env or credentials.json or token_*.json
3. NEVER share API Keys
4. NEVER edit .py files via GitHub web UI (error-003)

---

## Phase Roadmap
| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffolding | DONE |
| 1 | OAuth + Collector | BLOCKED - photos-only scope test pending |
| 2 | Vision EXIF+Gemini | PENDING |
| 3 | Cross-reference Sheets | PENDING Q2 unresolved |
| 4 | WebP Transform | CODE DONE |
| 5 | Drive + Notion log | NOTION_DATABASE_ID ready |
| 6 | Integration test | PENDING |

---

## Open Questions
| # | Question | Priority |
|---|----------|----------|
| Q2 | MAPLAB_Quotes sheet column names + date format? | HIGH |
| Q3 | Spouse OAuth done? token_spouse.json exist? | MEDIUM |

---

## Key Config
.env (all filled):
- MAPLAB_QUOTES_SHEET_ID: 1d2_SiEXh5JT4lzjkgHDI5JU9UWBY9TiPlC8DaxkQnKs
- GOOGLE_DRIVE_ARCHIVE_FOLDER_ID: 1L0udpuXLy3vEbHmzBbaLqNVDut2FFpCe
- GEMINI_API_KEY: see Notion API Keys page
- NOTION_TOKEN: see Notion API Keys page
- NOTION_DATABASE_ID: 320ab0806d5c801b9063d444cd7fbd1c

Auth:
- credentials.json: should exist at auth/credentials.json (created 2026-03-14)
- token_owner.json: DELETE BEFORE RE-AUTH

GCP:
- Publishing status: Production (實際運作中) ✅
- Photos Library API: Enabled ✅
- OAuth consent scopes: photoslibrary.readonly registered ✅
- client_id: 391140989706-8pvt19257iujvq1gd3flefn9tp3200cd.apps.googleusercontent.com

Code:
- google_auth.py: SCOPES = [photoslibrary.readonly only] — diagnostic build
- collector.py: FIXED (owner-only, timezone.utc, no em-dash)
- transformer.py: reads .env OK
- vision.py / crossref.py / archiver.py: skeletons pending
