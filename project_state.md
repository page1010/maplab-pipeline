# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.
>
> > NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.
> >
> > ---
> >
> > ## Last Updated
> > - Date: 2026-03-12
> > - - Updated by: Claude (Sonnet 4.6)
> >   - - Session: Block 3.6 - OAuth re-auth success, collector test pending
> >    
> >     - ---
> >
> > ## Project Goal
> > MAPLAB photos -> WebP SEO assets, cross-referenced with quotes/itineraries, logged to Notion. Original photos never deleted.
> >
> > ---
> >
> > ## Completed Tasks
> > | # | Task | By | Date |
> > |---|------|----|------|
> > | 0.1 | Project scaffolding | Claude | 2026-03-10 |
> > | 0.2 | AI handoff guide | Claude | 2026-03-10 |
> > | 0.3 | Python src skeleton | Claude | 2026-03-10 |
> > | 0.4 | .env.example + requirements.txt | Claude | 2026-03-10 |
> > | 0.5 | JSON schemas | Claude | 2026-03-10 |
> > | 1.1 | GCP project, 5 APIs enabled | Human | 2026-03-11 |
> > | 1.2 | credentials.json placed in auth/ | Human | 2026-03-11 |
> > | 1.3 | Gemini API Key -> .env | Human | 2026-03-11 |
> > | 2.1 | transformer.py reads .env | Claude | 2026-03-11 |
> > | 2.2 | pipeline.py wired Phase 1-5 | Claude | 2026-03-11 |
> > | 2.3 | test_transformer.py 14 tests | Claude | 2026-03-11 |
> > | 2.4-2.9 | Notion setup + API keys + ASSET_LOG | Claude | 2026-03-12 |
> > | 3.1 | OAuth owner confirmed | Human | 2026-03-12 |
> > | 3.2 | pip install complete | Human | 2026-03-12 |
> > | 3.3 | pipeline.py Phase 1 uncommented | Claude | 2026-03-12 |
> > | 3.4 | collector.py owner-only default 30d | Claude | 2026-03-12 |
> > | 3.5 | collector.py SyntaxError em-dash fixed | Claude | 2026-03-12 |
> > | 3.6 | OAuth re-auth with photoslibrary scope - Token valid | Human | 2026-03-12 |
> >
> > ---
> >
> > ## NEXT STEP - Run collector test to confirm Phase 1 DONE
> >
> > OAuth is complete. Token valid: True (expiry: 2026-03-12 11:25:54)
> > Just need to verify collector can actually fetch photos.
> >
> > ### Human run this command:
> > ```
> > cd Desktop\maplab-pipeline
> > python -m src.collector --test --account owner
> > ```
> >
> > Expected output:
> > ```
> > [owner] Fetching since YYYY-MM-DD to YYYY-MM-DD
> > [owner] API returned N items (keys: ['mediaItems', ...])
> > [owner] Queued: some_photo.jpg
> > Got 1 from owner
> > Fetched 1 photos
> >  - some_photo.jpg | YYYY-MM-DD | owner
> > ```
> >
> > If 0 photos: Check date range (may need --days 365 for old photos)
> > If still 403: Token scope issue, paste full error output
> >
> > ---
> >
> > ## Next AI Task (after human pastes collector output)
> > 1. Read this file + Notion
> > 2. 2. Human pastes: python -m src.collector --test --account owner output
> >    3. 3. If 1 photo fetched -> mark Phase 1 DONE, tick Notion checklist, commit
> >       4. 4. Then implement Phase 2: vision.py EXIF + Gemini
> >          5.    - Read EXIF from photo (GPS, camera model, datetime)
> >                -    - Call Gemini API for scene classification
> >                     -    - Return structured PhotoRecord with keywords + alt_text
> >                      
> >                          - ---
> >
> > ## SAFETY RULES
> > 1. NEVER delete original photos
> > 2. 2. NEVER commit .env
> >    3. 3. NEVER share API Keys page URL
> >      
> >       4. ---
> >      
> >       5. ## Phase Roadmap
> >       6. | Phase | Description | Status |
> >       7. |-------|-------------|--------|
> > | 0 | Scaffolding | DONE |
> > | 1 | OAuth + Collector | PENDING - run collector --test to confirm |
> > | 2 | Vision EXIF+Gemini | PENDING |
> > | 3 | Cross-reference Sheets | PENDING Q2 unresolved |
> > | 4 | WebP Transform | CODE DONE |
> > | 5 | Drive + Notion log | NOTION_DATABASE_ID ready |
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
- - GOOGLE_DRIVE_ARCHIVE_FOLDER_ID: 1L0udpuXLy3vEbHmzBbaLqNVDut2FFpCe
  - - GEMINI_API_KEY: see Notion API Keys page
    - - NOTION_TOKEN: see Notion API Keys page
    - NOTION_DATABASE_ID: 320ab0806d5c801b9063d444cd7fbd1c
   
    - Auth:
    - - token_owner.json: EXISTS - re-authed with photoslibrary scope - Token valid: True
      - - token_spouse.json: not confirmed
       
        - ASSET_LOG DB: https://www.notion.so/320ab0806d5c801b9063d444cd7fbd1c
       
        - Code status:
        - - pipeline.py: Phase 1 live
          - - collector.py: FIXED SyntaxError + owner-only + timezone.utc
            - - transformer.py: reads .env
              - - vision.py: skeleton Phase 2 TODO
                - - crossref.py: skeleton Q2 TBD
                  - - archiver.py: skeleton NOTION_DATABASE_ID ready
