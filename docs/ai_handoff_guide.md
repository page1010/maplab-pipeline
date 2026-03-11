# AI Handoff Guide

> This document defines the **collaboration protocol** for all AI assistants working on this project.  
> Whether you are Claude, GPT-4, or Gemini — follow this protocol exactly.

---

## 🔄 The Handoff Loop

Every AI session follows this loop:

```
START SESSION
    │
    ▼
1. Read project_state.md          ← mandatory, takes 30 seconds
    │
    ▼
2. Identify Current Task          ← listed in project_state.md
    │
    ▼
3. Do the work                    ← code, docs, analysis
    │
    ▼
4. Update project_state.md        ← mandatory before ending session
    │
    ▼
5. Commit changes to GitHub       ← with descriptive commit message
    │
    ▼
END SESSION → Next AI picks up from project_state.md
```

---

## 📝 How to Update project_state.md

At the end of every session, update these sections:

### 1. Last Updated
```markdown
- **Date:** YYYY-MM-DD
- **Updated by:** [Claude / GPT-4o / Gemini Pro] (model name + version)
- **Session type:** [Implementation / Debug / Review / Documentation]
```

### 2. Move completed items to Completed Tasks table
```markdown
| 1.2 | Implemented OAuth token refresh | Claude Sonnet 4.6 | 2026-03-11 |
```

### 3. Update Current Task
Be specific. Include:
- What was done this session
- What the next person needs to run/test
- Any blockers

### 4. Update Open Questions
- Close answered questions (mark ✅ RESOLVED)
- Add new questions discovered during work

---

## 🎯 Recommended AI for Each Phase

| Phase | Recommended Model | Reason |
|-------|------------------|--------|
| Phase 1: OAuth + Collector | Claude or GPT-4o | Complex auth logic, needs careful error handling |
| Phase 2: Vision + EXIF | Claude or Gemini | Gemini knows its own API best; Claude for code quality |
| Phase 3: Cross-reference | GPT-4o or Claude | Logic-heavy date matching, needs reasoning |
| Phase 4: WebP Transform | GPT-4o mini or Gemini Flash | Mechanical task, use cheaper model |
| Phase 5: Drive + Notion | Claude | API integration, error handling |
| Phase 6: Integration | Claude | Orchestration, debugging |

---

## 📋 Session Start Prompt Template

Copy this when starting a new AI session:

```
You are an AI developer collaborator on the MAPLAB Digital Asset Pipeline project.

MANDATORY FIRST STEP: Read the file `project_state.md` in this repository. It contains:
- Current task to work on
- What has been completed
- Open questions
- File map of the repository

After reading project_state.md, do ONLY the Current Task listed there.
At the end of your work, update project_state.md with your progress.

Repository context: [paste relevant files or link to GitHub repo]
```

---

## 🚫 What NOT to Do

- ❌ Do NOT start coding without reading `project_state.md` first
- ❌ Do NOT refactor code from previous phases without noting it in state
- ❌ Do NOT leave the session without updating `project_state.md`
- ❌ Do NOT change the file naming convention or schema without documenting it
- ❌ Do NOT use synchronous blocking calls — this pipeline may process 500+ photos

---

## ✅ Code Quality Standards

- All functions must have docstrings
- All API calls must have try/except with specific error types
- Log everything to `pipeline.log` (not print statements)
- Use `python-dotenv` for all credentials — never hardcode
- Date format throughout: `YYYYMMDD` (no separators in filenames)

---

## 🔗 GitHub Commit Convention

```
[PHASE-X] Brief description

Examples:
[PHASE-1] Add OAuth2 token refresh logic
[PHASE-2] Gemini prompt v2 - improved keyword extraction  
[FIX] Handle missing EXIF GPS gracefully
[DOCS] Update architecture diagram
[STATE] Update project_state.md after session
```

---

*This guide was initialized by Claude on 2026-03-10.*
