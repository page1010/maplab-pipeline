# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.
>
> > NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.

---

## Last Updated
- Date: 2026-03-15 (session complete — GCP fully configured, PRs open)
- Updated by: Claude (Sonnet 4.6) — A4 Pipeline Agent
- Session: Research + two branches + GCP maplab-v2 fully set up.

---

## ⚠️ ROOT CAUSE CONFIRMED — API DEPRECATION

**photoslibrary.readonly was OFFICIALLY REMOVED by Google on 2025-03-31.**
All 403 errors were caused by this. NOT a code bug. NOT a GCP config issue.
The scope simply does not exist anymore.

---

## GCP maplab-v2 — Current Status ✅ READY FOR PLAN A TEST

| Component | Status |
|-----------|--------|
| Project | maplab-v2 ✅ |
| Publishing Mode | Testing ✅ |
| Google Photos Picker API | ✅ ENABLED |
| OAuth Consent Screen | ✅ Created (MAPLAB Pipeline, External) |
| Scope: photospicker.mediaitems.readonly | ✅ Added (機密範圍) |
| Test User: pagewu1010@gmail.com | ✅ Added (1/100) |
| OAuth Client: maplab-v2-desktop | ✅ Created (Desktop App) |
| Client ID | 303909948610-fo90n8v7c1u0gvh4lbakkhkcofad12va.apps.googleusercontent.com |
| Client Secret | ****3ufQ (download JSON from GCP console to get full secret) |

**To get credentials.json:**
1. Go to: console.cloud.google.com/auth/clients?project=maplab-v2
2. Click maplab-v2-desktop -> Download JSON (⬇ icon)
3. Save as auth/credentials.json
4. NEVER commit this file (already in .gitignore)

---

## Open Branches & PRs

| Branch | Plan | PR | Status |
|--------|------|-----|--------|
| work/pipeline/a4/feat-picker-api | Plan A: Picker API | #3 | 🟡 GCP ready, needs git pull + test |
| work/pipeline/a4/feat-local-source | Plan B: rclone/local | #4 | 🟡 Needs rclone setup |

---

## NEXT STEPS — Ordered by Priority

### Step 1 (HUMAN — 2 minutes): Get new credentials.json
1. Go to console.cloud.google.com/auth/clients?project=maplab-v2
2. Click maplab-v2-desktop row -> Download JSON button (⬇)
3. Copy downloaded file to: maplab-pipeline/auth/credentials.json
4. (DO NOT commit it)

### Step 2 (HUMAN — 1 minute): Update local repo
```
cd C:\Users\USER GT3490\Desktop\maplab-pipeline
git stash         (or: git checkout -- auth/setup_credentials.py src/auth/google_auth.py)
git pull origin main
```

### Step 3 (HUMAN — Plan A test): Run Picker API collector
```
del auth\token_picker.json   (if exists)
python -m src.collector_picker --test
```
Browser will open -> select 1-5 photos in Google Photos UI -> script prints results.
Expected: "Fetched: N items" where N > 0.

### Step 4 (HUMAN — Plan B test, optional): rclone setup
```
winget install Rclone.Rclone
rclone config
  -> New remote -> name: gphotos -> type: google photos -> read_only: true
rclone mount gphotos:media/by-month/ %USERPROFILE%\mnt\gphotos --vfs-cache-mode full
```
Add to .env: LOCAL_PHOTOS_PATH=%USERPROFILE%\mnt\gphotos
Then: python -m src.collector_local --test

### Step 5 (AGENT after test): Merge winner PR + Phase 2
After either test passes:
- Update this file
- Merge winning PR (#3 or #4)
- Start Phase 2: vision.py (WebP conversion)

---

## Research Summary

| Topic | Finding |
|-------|---------|
| photoslibrary.readonly | REMOVED 2025-03-31 |
| Official replacement | Google Photos Picker API |
| New scope | photospicker.mediaitems.readonly |
| New endpoint | photospicker.googleapis.com/v1/sessions |
| Alternative | rclone mount (no OAuth needed) |
| Community | 100s of SO questions in 2025 about same 403 issue |

---

## Completed Tasks
| # | Task | By | Date |
|---|------|----|------|
| 0.1-3.14 | Previous sessions (scaffolding, OAuth debug) | Claude | 2026-03-10~14 |
| 4.1 | Session postmortem | Claude | 2026-03-14 |
| 4.2 | Research: API deprecation confirmed | Claude | 2026-03-15 |
| 4.3 | Branch A: feat-picker-api | Claude | 2026-03-15 |
| 4.4 | Branch B: feat-local-source | Claude | 2026-03-15 |
| 4.5 | src/collector_picker.py (Plan A) | Claude | 2026-03-15 |
| 4.6 | src/collector_local.py (Plan B) | Claude | 2026-03-15 |
| 4.7 | PR #3 (Plan A) + PR #4 (Plan B) opened | Claude | 2026-03-15 |
| 4.8 | GCP maplab-v2: Picker API enabled | Claude | 2026-03-15 |
| 4.9 | GCP maplab-v2: Test user added | Claude | 2026-03-15 |
| 4.10 | GCP maplab-v2: photospicker scope added | Claude | 2026-03-15 |
| 4.11 | GCP maplab-v2: OAuth client created (maplab-v2-desktop) | Claude | 2026-03-15 |

---

## Error Log (Updated)

| Error ID | Error | Root Cause | Fix | Date |
|----------|-------|-----------|-----|------|
| error-001~004 | Various IndentationError + 403s | See previous entries | Fixed | 2026-03-13~14 |
| error-005 | Switched GCP to Production | Mistake | New project maplab-v2 | 2026-03-14 |
| error-006~007 | 403 "insufficient authentication scopes" | **photoslibrary.readonly REMOVED 2025-03-31** | **Migrate to Picker API (Plan A) or rclone (Plan B)** | 2026-03-15 |
| error-008 | Cannot revert Production → Testing | GCP policy | New project | 2026-03-14 |
| error-009 | git pull blocked | Uncommitted local files | git stash + pull | 2026-03-14 |

---

## SAFETY RULES
1. NEVER delete original photos
2. NEVER commit .env or credentials.json or token_*.json
3. NEVER share API Keys  
4. NEVER edit .py files via GitHub web UI
5. NEVER switch GCP from Testing to Production without full verification

---

## Phase Roadmap
| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffolding | DONE |
| 1 | Photo Source | 🟡 GCP ready, awaiting local test |
| 2 | Vision / WebP | Not started |
| 3 | Notion logging | Not started |
| 4 | Full pipeline | Not started |
