# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.
>
> > NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.

---

## Last Updated
- Date: 2026-03-15 (morning — Phase 2 planning + branch creation)
- Updated by: Claude (Sonnet 4.6) — A4 Pipeline Agent
- Session: Research report compiled. Two solution branches opened. Code committed.

---

## Project Goal
MAPLAB photos -> WebP SEO assets, cross-referenced with quotes/itineraries, logged to Notion. Original photos never deleted.

---

## ⚠️ ROOT CAUSE CONFIRMED — API DEPRECATION (NOT A CODE BUG)

**photoslibrary.readonly was OFFICIALLY REMOVED by Google on 2025-03-31.**

This is why we have been getting 403 "insufficient authentication scopes" for months.
It has nothing to do with GCP Production/Testing mode, OAuth client, or code quality.
The scope simply does not exist anymore.

Sources:
- developers.google.com/photos/support/updates (official Google docs)
- stackoverflow.com/questions/tagged/google-photos-api (community confirmation)
- developers.googleblog.com announcement (September 2024)

---

## Research Report — Google Photos API Status (2026-03-15)

### Timeline
| Event | Date |
|-------|------|
| Picker API launched | 2024-09-18 |
| Deprecation announced | 2024-09-18 |
| photoslibrary.readonly REMOVED | 2025-03-31 |
| Our project started debugging | 2026-03-14 (one year after removal) |

### Removed Scopes (dead, returns 403 always)
- photoslibrary.readonly ❌
- photoslibrary.sharing ❌
- photoslibrary ❌

### Surviving Scopes (still valid)
- photoslibrary.appendonly ✅ (upload only, app-created content)
- photoslibrary.readonly.appcreateddata ✅ (read only app-created content)
- photoslibrary.edit.appcreateddata ✅ (edit app-created content)
- **photospicker.mediaitems.readonly ✅ (NEW — Picker API, user-interactive)**

### API Summary
| API | Endpoint | Use Case | MAPLAB Fit |
|-----|---------|---------|-----------|
| Library API | photoslibrary.googleapis.com | Upload/manage app-created photos | ❌ |
| **Picker API** | photospicker.googleapis.com | User picks photos from their library | ⚠️ Semi-auto |
| Ambient API | — | Smart TV / photo frame slideshow | ❌ |

---

## Solution Plan

### Plan A — Picker API (Branch: work/pipeline/a4/feat-picker-api)
**Status: 🟡 Code committed, PR open, needs maplab-v2 GCP scope setup + human test**

How it works:
1. Python script creates a Picker Session
2. Opens pickerUri in browser — user selects photos in Google Photos UI
3. Script polls until selection complete
4. Script downloads selected MediaItems via Picker API

New scope: https://www.googleapis.com/auth/photospicker.mediaitems.readonly
New endpoint: https://photospicker.googleapis.com/v1/sessions

Files changed:
- src/collector_picker.py (NEW)

Pros: Official Google solution. Will work permanently.
Cons: Requires user interaction each run (not fully headless).
Best for: Batch runs where user manually kicks off the pipeline.

GCP Setup needed (once):
- Enable "Google Photos Picker API" in GCP console (different from Photos Library API)
- Add scope: photospicker.mediaitems.readonly in OAuth consent screen
- Create new token (del auth/token_picker.json if exists, then run collector_picker.py)

### Plan B — Local Source / rclone (Branch: work/pipeline/a4/feat-local-source)
**Status: 🟡 Code committed, PR open, needs rclone install + mount (human, one-time)**

How it works:
1. Install rclone (one-time, human)
2. rclone config -> add Google Photos remote
3. Mount: rclone mount gphotos:media/by-month/... ~/mnt/gphotos --vfs-cache-mode full
4. Set LOCAL_PHOTOS_PATH=~/mnt/gphotos in .env
5. Run: python -m src.collector_local (fully automated, no OAuth)

Files changed:
- src/collector_local.py (NEW)

Pros: Fully headless. No OAuth. No Google API policy. Runs on schedule (cron).
Cons: rclone mount stays running as background process. Mount restarts on reboot.
Best for: Fully automated pipeline with no user interaction.

---

## Open Branches

| Branch | Plan | Status | PR |
|--------|------|--------|-----|
| work/pipeline/a4/feat-picker-api | Plan A: Picker API | 🟡 Code ready, PR open | #3 |
| work/pipeline/a4/feat-local-source | Plan B: rclone/local | 🟡 Code ready, PR open | #4 |

---

## Completed Tasks
| # | Task | By | Date |
|---|------|----|------|
| 0.1 | Project scaffolding | Claude | 2026-03-10 |
| 0.2 | AI handoff guide | Claude | 2026-03-10 |
| 0.3 | Python src skeleton | Claude | 2026-03-10 |
| 1.1 | google_auth.py (OAuth2 flow) | Claude | 2026-03-10 |
| 1.2 | collector.py (Photos API) | Claude | 2026-03-10 |
| 2.1 | AGENT_RULES.md v1.0 | Claude | 2026-03-10 |
| 2.2 | AGENT_RULES.md v1.3 update | Claude | 2026-03-13 |
| 3.1-3.14 | Debug sessions (OAuth, GCP, scope) | Claude | 2026-03-13~14 |
| 4.1 | Session postmortem documented | Claude | 2026-03-14 |
| 4.2 | Research: API deprecation confirmed | Claude | 2026-03-15 |
| 4.3 | Branch A created: feat-picker-api | Claude | 2026-03-15 |
| 4.4 | Branch B created: feat-local-source | Claude | 2026-03-15 |
| 4.5 | src/collector_picker.py committed (Plan A) | Claude | 2026-03-15 |
| 4.6 | src/collector_local.py committed (Plan B) | Claude | 2026-03-15 |
| 4.7 | PR #3 opened (Plan A), PR #4 opened (Plan B) | Claude | 2026-03-15 |

---

## NEXT AI TASK — START HERE

### Priority 1: Test Plan B (rclone) — recommended path
Human one-time setup:
1. Install rclone: https://rclone.org/install/ (Windows: winget install Rclone.Rclone)
2. Run: rclone config
   - New remote -> name: gphotos -> type: google photos
   - Follow OAuth prompts (browser opens, sign in to Google)
   - read_only: true
3. Test mount: rclone ls gphotos:media/by-month/
4. Mount: rclone mount gphotos:media/by-month/ %USERPROFILE%\mnt\gphotos --vfs-cache-mode full
5. Add to .env: LOCAL_PHOTOS_PATH=%USERPROFILE%\mnt\gphotos
6. git pull origin main (after PR #4 merges)
7. python -m src.collector_local --test

### Priority 2: Test Plan A (Picker API) — if Plan B not feasible
GCP setup (agent can do):
- Navigate to console.cloud.google.com/apis/library
- Search "Google Photos Picker API" -> Enable for maplab-v2
- Add scope photospicker.mediaitems.readonly to OAuth consent screen
- Human test: python -m src.collector_picker --test (browser opens, select 1 photo)

### Priority 3: Merge whichever plan works first
Agent task after successful test:
- Update project_state.md (this file) with results
- Merge winning branch PR
- Update Phase 1 status to DONE
- Start Phase 2: vision.py (WebP conversion)

---

## Error Log

| Error ID | Error | Root Cause | Fix | Date |
|----------|-------|-----------|-----|------|
| error-001 | IndentationError google_auth.py line 78 | GitHub web editor corrupted indentation | PR #1 via GitHub API | 2026-03-13 |
| error-002 | IndentationError setup_credentials.py line 24 | Same cause | PR #1 via GitHub API | 2026-03-13 |
| error-003 | git reset --hard didn't fix local | Corrupted files in committed history | git checkout origin/main | 2026-03-13 |
| error-004 | 403 PERMISSION_DENIED (no scope in token) | Old token had no photos scope | Delete token + prompt=consent | 2026-03-14 |
| error-005 | MISTAKE: Changed GCP to Production | Misdiagnosed 500 error root cause | Created new project maplab-v2 (Testing) | 2026-03-14 |
| error-006 | 500 Internal Server Error on OAuth | Production + multiple Restricted Scopes | Reduced to photos-only (PR #2) | 2026-03-14 |
| error-007 | 403 "insufficient authentication scopes" | **photoslibrary.readonly REMOVED 2025-03-31** | **Migrate to Picker API or rclone** | 2026-03-15 |
| error-008 | Cannot revert Production to Testing | GCP policy: once >100 users locked | New project maplab-v2 | 2026-03-14 |
| error-009 | git pull aborted — local changes | Local files modified, uncommitted | git stash + git pull | 2026-03-14 |

---

## SAFETY RULES
1. NEVER delete original photos
2. NEVER commit .env or credentials.json or token_*.json
3. NEVER share API Keys
4. NEVER edit .py files via GitHub web UI (causes IndentationError)
5. NEVER switch GCP app from Testing to Production unless fully verified

---

## Phase Roadmap
| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffolding | DONE |
| 1 | Photo Source (OAuth + Collector) | 🟡 IN PROGRESS — Plan A & B branched |
| 2 | Vision / WebP conversion | Not started |
| 3 | Notion logging | Not started |
| 4 | Full pipeline run | Not started |
