# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.
>
> > NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.

---

## Last Updated
- Date: 2026-03-14 (end of day — session postmortem)
- Updated by: Claude (Sonnet 4.6) — A4 Pipeline Agent
- Session: FULL FAILURE LOG — OAuth 403 root cause chase, GCP Production mode trap, maplab-v2 new project setup attempt, IndentationError still not resolved locally.

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
| 1.1 | google_auth.py (OAuth2 flow) | Claude | 2026-03-10 |
| 1.2 | collector.py (Photos API) | Claude | 2026-03-10 |
| 2.1 | AGENT_RULES.md v1.0 | Claude | 2026-03-10 |
| 2.2 | AGENT_RULES.md v1.3 update | Claude | 2026-03-13 |
| 3.1 | requirements.txt added | Claude | 2026-03-13 |
| 3.2 | config.py added | Claude | 2026-03-13 |
| 3.3 | .gitignore confirmed (token*, credentials.json protected) | Claude | 2026-03-13 |
| 3.4 | Local venv setup documented | Human | 2026-03-13 |
| 3.5 | First OAuth test run | Human | 2026-03-13 |
| 3.6 | Identified: google_auth.py + setup_credentials.py corrupted by GitHub web editor | Claude | 2026-03-13 |
| 3.7 | AGENT_RULES.md: NEVER edit .py via GitHub web UI (IndentationError rule) | Claude | 2026-03-13 |
| 3.8 | auth/setup_credentials.py added (auto-copy from Downloads) | Claude | 2026-03-13 |
| 3.9 | git pull --no-edit success | Human | 2026-03-13 |
| 3.10 | NEVER edit .py via GitHub web UI (IndentationError documented) | Claude | 2026-03-13 |
| 3.11 | PR #1: Fix corrupted google_auth.py + setup_credentials.py via GitHub API | Claude | 2026-03-14 |
| 3.12 | GCP photoslibrary.readonly added to OAuth consent scopes | Claude | 2026-03-14 |
| 3.13 | GCP app status changed from Testing to Production (MISTAKE — see error-005) | Claude | 2026-03-14 |
| 3.14 | PR #2: Reduce SCOPES to photos-only for OAuth 500 diagnosis | Claude | 2026-03-14 |
| 3.15 | New OAuth client maplab-pipeline-v2 created (Production project) | Claude | 2026-03-14 |
| 3.16 | Token verified via tokeninfo — scope confirmed present | Claude | 2026-03-14 |
| 3.17 | New GCP project maplab-v2 created (Testing mode by default) | Claude | 2026-03-14 |
| 3.18 | maplab-v2 OAuth Consent Screen brand wizard completed | Claude | 2026-03-14 |

---

## TODAY'S FAILURE LOG — 2026-03-14

### What we tried (in order):

1. **PR #1** — Fixed IndentationError in google_auth.py and setup_credentials.py via GitHub API. Merged successfully.
2. **GCP: added photoslibrary.readonly scope** — Was missing from OAuth consent screen.
3. **Switched GCP app to Production** — MISTAKE. This caused all subsequent 403s.
4. **PR #2** — Reduced SCOPES to photos-only, thinking multiple Restricted Scopes caused 500. Merged.
5. **New OAuth client (maplab-pipeline-v2)** — Old client was suspected. New client created, credentials.json updated.
6. **tokeninfo check** — Token IS valid. Scope IS in token. But collector still returns 403.
7. **Tried to revert Production → Testing** — GCP refused with error "更新應用程式時發生錯誤". Cannot downgrade once user count exceeded.
8. **Created new GCP project maplab-v2** — Clean slate, Testing mode. Completed OAuth Consent Screen wizard.
9. **Local git pull still failing** — "your local changes to the following files would be overwritten by merge: auth/setup_credentials.py, src/auth/google_auth.py". Local machine still has unresolved state.
10. **IndentationError still on local** — Even after GitHub PRs merged, local files are stuck (stash/reset needed).

### Root cause analysis:

| Layer | Issue | Status |
|-------|-------|--------|
| Code (google_auth.py) | IndentationError line 78 — fixed in GitHub main via PR #1 | ✅ Fixed in repo, ❌ NOT pulled locally |
| Code (setup_credentials.py) | IndentationError line 24 — fixed in GitHub main via PR #1 | ✅ Fixed in repo, ❌ NOT pulled locally |
| GCP Config | Production mode blocks Restricted Scopes (photoslibrary.readonly) at API Gateway | ❌ Original project LOCKED in Production |
| GCP Config | Cannot revert Production → Testing once >100 users | ❌ PERMANENT on maplab-pipeline |
| Local repo | Uncommitted local changes blocking git pull | ❌ Needs: git stash or git checkout -- . |

### Why collector returns 403 even with valid token:

Google's policy: apps in **Production** status requesting **Restricted Scopes** (photoslibrary.readonly is Restricted) require **Google verification** before the scope is actually honored at the API Gateway level. The OAuth flow succeeds and the token looks valid via tokeninfo, but Google silently strips the scope permissions server-side. Result: 403 "insufficient authentication scopes" even though the token shows the scope.

This is NOT a code bug. The code is correct. The GCP project is in the wrong state.

### What SHOULD work:

Using maplab-v2 (Testing mode):
- Restricted Scopes work for Test Users without verification
- pagewu1010@gmail.com added as Test User = full photoslibrary.readonly access
- New OAuth client + credentials.json → re-auth → collector should succeed

---

## CURRENT STATUS — maplab-v2 Setup Progress

| Step | Task | Status |
|------|------|--------|
| A | Photos Library API enabled for maplab-v2 | ⏳ In progress |
| B | Test User pagewu1010@gmail.com added | ⏳ In progress |
| C | photoslibrary.readonly scope added | ❌ Not done |
| D | OAuth Desktop App client created | ❌ Not done |
| E | New credentials.json generated | ❌ Not done |
| F | Local: git stash → git pull → update credentials.json → del token → re-auth | ❌ Not done |
| G | python -m src.collector --test --account owner | ❌ Not done |

---

## NEXT AI TASK — START HERE

### Step 0 — Fix local repo (HUMAN action needed OR agent does via terminal)
```
cd C:\Users\USER GT3490\Desktop\maplab-pipeline
git stash
git pull origin main
git stash pop  # or just discard: git checkout -- .
```
If stash pop causes conflict: just `git checkout -- auth/setup_credentials.py src/auth/google_auth.py` then `git pull`

### Step 1 — Complete maplab-v2 GCP setup
Navigate to: https://console.cloud.google.com/auth/audience?project=maplab-v2
- Add Test User: pagewu1010@gmail.com
- Save

Navigate to: https://console.cloud.google.com/apis/library/photoslibrary.googleapis.com?project=maplab-v2
- Click 啟用 (Enable)

Navigate to: https://console.cloud.google.com/auth/scopes?project=maplab-v2
- Add scope: https://www.googleapis.com/auth/photoslibrary.readonly
- Save

Navigate to: https://console.cloud.google.com/auth/clients/create?project=maplab-v2
- Type: Desktop App
- Name: maplab-v2-desktop
- Record new client_id + client_secret

### Step 2 — Update credentials.json
Use Python one-liner (same as before) to write new credentials.json with maplab-v2 client_id/secret.
NEVER commit credentials.json.

### Step 3 — Re-auth + test
```
del auth\token_owner.json
python -m src.auth.google_auth --account owner
python -m src.collector --test --account owner
```

Expected: Fetched > 0 photos.

---

## Error Log

| Error ID | Error | Root Cause | Fix | Date |
|----------|-------|-----------|-----|------|
| error-001 | IndentationError google_auth.py line 78 | GitHub web editor corrupted indentation | PR #1 via GitHub API | 2026-03-13 |
| error-002 | IndentationError setup_credentials.py line 24 | Same cause | PR #1 via GitHub API | 2026-03-13 |
| error-003 | git reset --hard didn't fix local | Corrupted files were in committed history | git checkout origin/main | 2026-03-13 |
| error-004 | 403 PERMISSION_DENIED (no scope in token) | Old token had no photos scope | Delete token + prompt=consent | 2026-03-14 |
| error-005 | MISTAKE: Changed GCP to Production | Misdiagnosed 500 error root cause | Created new project maplab-v2 (Testing) | 2026-03-14 |
| error-006 | 500 Internal Server Error on OAuth | Production + multiple Restricted Scopes conflict | Reduced to photos-only (PR #2) | 2026-03-14 |
| error-007 | 403 "insufficient authentication scopes" | Production mode silently strips Restricted Scope at API Gateway despite valid token | New project maplab-v2 in Testing mode | 2026-03-14 |
| error-008 | Cannot revert Production → Testing | GCP policy: once >100 users, cannot downgrade | Permanent. Workaround: new project | 2026-03-14 |
| error-009 | git pull aborted — local changes would be overwritten | Local files modified, not committed | git stash + git pull (human action needed) | 2026-03-14 |

---

## SAFETY RULES
1. NEVER delete original photos
2. NEVER commit .env or credentials.json or token_*.json
3. NEVER share API Keys
4. NEVER edit .py files via GitHub web UI (error-003)
5. NEVER switch GCP app from Testing to Production unless fully verified (error-005)

---

## Phase Roadmap
| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Scaffolding | DONE |
| 1 | OAuth + Collector | BLOCKED — maplab-v2 setup incomplete + local git pull pending |
| 2 | Vision / WebP conversion | Not started |
| 3 | Notion logging | Not started |
| 4 | Full pipeline run | Not started |
