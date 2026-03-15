# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.
>
> > NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.

---

## Last Updated
- Date: 2026-03-15 (midday — Phase 1 complete, architecture pivot, re-planning)
- Updated by: Claude (Sonnet 4.6) — A4 Pipeline Agent
- Session: Plan A (Picker API) confirmed working. Architecture pivoted to Google Drive as primary photo source per team recommendation.

---

## ✅ Phase 1 SUCCESS LOG — What We Proved Works

| Item | Result |
|------|--------|
| Picker API OAuth flow | ✅ Works — token saved, scope confirmed |
| Session create/poll/delete | ✅ Works |
| Photo metadata returned | ✅ filename, mimeType, width, height, createTime, type |
| First real photo fetched | ✅ Screenshot_2026-03-10-16-23-31-060_com.google.android.youtube.jpg (image/jpeg) [PHOTO] 2400x1080 |
| GCP maplab-v2 (Testing mode) | ✅ Stable — Picker API enabled, scope set, test user added |

---

## ⚠️ Architecture Pivot — Google Photos API → Google Drive

### Why we changed
1. Google Photos photoslibrary.readonly was **removed 2025-03-31** — no batch read possible
2. Picker API requires user interaction every run — not suitable for automated pipeline
3. Other project agents also hit permission walls asking user repeatedly
4. **Team recommendation**: store photos in Google Drive folder instead, pipeline reads from there
5. New photos will be saved directly to Google Drive folder — simpler, reliable, no API policy risk

### New Data Flow
```
[User saves photos] → [Google Drive folder] → [collector_drive.py reads] 
  → [vision.py: EXIF + Gemini analysis] → [transformer.py: WebP convert]
  → [archiver.py: save to Drive output folder] → [Notion log]
```

### Old Data Flow (retired)
```
[Google Photos] → [Picker API / Library API] → collector.py → ...
```

---

## Current Codebase State

### src/ files

| File | Status | Notes |
|------|--------|-------|
| collector.py | 🔴 Retired | Used photoslibrary.readonly (removed) |
| collector_picker.py | ✅ Working | Picker API — for on-demand selective use |
| collector_local.py | ✅ Working | Reads local/rclone path — for rclone users |
| **collector_drive.py** | ❌ TODO | NEW: read from Google Drive folder |
| vision.py | 🟡 Skeleton | EXIF + Gemini analysis — needs wiring |
| transformer.py | 🟡 Skeleton | WebP conversion — needs wiring |
| archiver.py | 🟡 Skeleton | Drive upload — likely needs update for new folder structure |
| crossref.py | 🟡 Skeleton | Cross-reference with quotes sheet |
| pipeline.py | 🟡 Skeleton | Orchestrator — needs new collector wired in |

### docs/
- ai_handoff_guide.md — agent onboarding
- architecture.md — needs update for new flow
- naming_rules.md
- prompts.md

### .env.example (key vars)
- GOOGLE_DRIVE_ARCHIVE_FOLDER_ID — root output folder ✅ already planned
- MAPLAB_QUOTES_SHEET_ID — quotes cross-ref ✅ already planned
- GEMINI_API_KEY — AI analysis ✅ already planned

---

## New Phased Roadmap

### Phase 1 — Photo Source ✅ DONE (pivot confirmed)
- ✅ Proved Picker API works (backup option)
- ✅ collector_local.py ready (rclone option)
- ✅ Architecture decision: Google Drive as primary source

### Phase 2 — Google Drive Collector (CURRENT)
Goal: collector_drive.py reads photos from a specified Drive folder
Tech: Google Drive API v3 (drive.readonly scope — NOT restricted, standard API)
Scope: https://www.googleapis.com/auth/drive.readonly

Steps (agent does all in cloud):
1. Create branch work/pipeline/a4/feat-drive-collector
2. Write src/collector_drive.py
   - Auth via google-auth with drive.readonly scope
   - List files in GOOGLE_DRIVE_PHOTOS_FOLDER_ID (new .env var)
   - Filter by mimeType image/*
   - Download to temp dir
   - Return list of local paths + metadata
3. Update .env.example with GOOGLE_DRIVE_PHOTOS_FOLDER_ID
4. Update google_auth.py to support drive scope (new token file)
5. PR + merge
6. Human test: set folder ID in .env, run python -m src.collector_drive --test

### Phase 3 — Vision Pipeline
Goal: For each photo, extract EXIF + run Gemini analysis
- vision.py already has skeleton
- Needs: download URL → PIL open → EXIF → Gemini describe → return structured metadata

### Phase 4 — Transform + Archive
Goal: Convert to WebP, upload to Drive output folder
- transformer.py: Pillow WebP conversion
- archiver.py: upload to GOOGLE_DRIVE_ARCHIVE_FOLDER_ID
- Naming: {date}_{original_name}_maplab.webp

### Phase 5 — Notion Logging
Goal: Log each processed photo to Notion database
- Create Notion page per photo with metadata, Gemini description, Drive link

### Phase 6 — Full Pipeline Run
Goal: python -m src.pipeline runs end-to-end unattended

---

## GCP Status Summary

| Project | Status | Use |
|---------|--------|-----|
| maplab-pipeline (OLD) | ⚠️ Production, locked | Retired — do not use |
| maplab-v2 | ✅ Testing | Picker API client (backup use) |

Drive API uses same OAuth client (maplab-v2-desktop) — drive.readonly is a standard (non-restricted) scope, no Google verification needed.

---

## NEXT AI TASK — START HERE

**Task: Build collector_drive.py (Phase 2)**

1. Create branch: work/pipeline/a4/feat-drive-collector
2. Write src/collector_drive.py with Drive API v3
3. Update auth/google_auth.py — add drive.readonly to supported scopes (new token: token_drive.json)
4. Update .env.example — add GOOGLE_DRIVE_PHOTOS_FOLDER_ID
5. Open PR, merge
6. Update this file

Human action needed after merge:
- Set GOOGLE_DRIVE_PHOTOS_FOLDER_ID in .env (get folder ID from Drive URL)
- python -m src.collector_drive --test

---

## Success Credentials (DO NOT COMMIT)

| Item | Value |
|------|-------|
| GCP Project | maplab-v2 |
| OAuth Client | maplab-v2-desktop |
| Client ID | 303909948610-fo90n8v7c1u0gvh4lbakkhkcofad12va.apps.googleusercontent.com |
| Token files | auth/token_picker.json, auth/token_drive.json (after Phase 2) |
| credentials.json | auth/credentials.json (maplab-v2-desktop) |

---

## Error Log (Final — Phase 1)

| ID | Error | Root Cause | Resolution |
|----|-------|-----------|-----------|
| error-001~003 | IndentationError | GitHub web editor | Fixed via GitHub API PR #1 |
| error-004~008 | 403 on photoslibrary.readonly | Scope removed 2025-03-31 + Production mode | Architecture pivot to Drive |
| error-009 | git pull blocked | Local uncommitted files | git stash + pull |
| error-010 | collector_picker None fields | Picker API nested structure (item.mediaFile.*) | Fixed in commit 22d4e38 |

---

## SAFETY RULES
1. NEVER delete original photos
2. NEVER commit .env, credentials.json, token_*.json
3. NEVER edit .py via GitHub web UI
4. NEVER push directly to main — branch + PR only
5. NEVER switch GCP to Production without full verification
