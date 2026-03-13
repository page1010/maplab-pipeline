# PROJECT STATE
AI Collaborator: Read this file FIRST. Update this file LAST.

> Work Rules: Before each session read this file + Notion + GitHub. After: update this file. Only run blocks needing no human action. Split small steps, each step = 1 commit.
>
> > NO-DELETE RULE: Never delete original photos. Pipeline reads->converts copy->uploads copy->logs. Source never touched.
> >
> > ---
> >
> > ## Last Updated
> > - Date: 2026-03-13
> > - - Updated by: Claude (Sonnet 4.6)
> >   - - Session: Block 3.9 - git pull success (use --no-edit to skip vim); next: setup_credentials.py + re-auth
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
> > | 3.6 | google_auth.py prompt=consent fix (Gemini diagnosis) | Claude | 2026-03-12 |
> > | 3.7 | New OAuth client + credentials.json re-downloaded | Human | 2026-03-13 |
> >  | 3.8 | auth/setup_credentials.py added (auto-copy from Downloads) | Claude | 2026-03-13 |
> >  | 3.9 | git pull --no-edit success; vim tip: :q! or --no-edit flag | Human | 2026-03-13 |
> >
> > ---
> > ## CURRENT BLOCKER - 1 command only
> >
> > auth/ folder was empty (credentials.json + token_owner.json both gone).
> > New OAuth client created: maplab-pipeline-desktop
> > new client_id: 391140989706-8pvt19257iujvq1gd3flefn9tp3200cd.apps.googleusercontent.com
> >
> > Step 1 - Auto-copy credentials.json (no manual rename/move):
> >   cd Desktop\maplab-pipeline
> > > >   git pull origin main
> > > > > >   python auth/setup_credentials.py
> > > > > > > >   (Script finds client_secret_391140...json in Downloads and copies to auth/ automatically)
> >
> > Step 2 - Re-auth (prompt=consent will force FULL consent screen):
> >   cd Desktop\maplab-pipeline
> >   python -m src.auth.google_auth --account owner
> >   Browser opens -> click Advanced -> Go to maplab-pipeline (unsafe) -> Allow ALL
> >
> > Step 3 - Verify:
> >   python -m src.collector --test --account owner
> >   Expected: Fetched 1 photos
> >
> > ---
> >
> > ## Next AI Task
> > 1. Read this file + Notion
> > 2. 2. Human pastes collector --test output
> >    3. 3. If Fetched 1 photos -> Phase 1 DONE, commit, update Notion
> >       4. 4. Start Phase 2: vision.py EXIF + Gemini
> >         
> >          5. ---
> >         
> >          6. ## SAFETY RULES
> >          7. 1. NEVER delete original photos
> >             2. 2. NEVER commit .env or credentials.json or token_*.json
> > 3. NEVER share API Keys page URL
> >
> > 4. ---
> >
> > 5. ## Phase Roadmap
> > 6. | Phase | Description | Status |
> > 7. |-------|-------------|--------|
> > 8. | 0 | Scaffolding | DONE |
> > 9. | 1 | OAuth + Collector | BLOCKED - run setup_credentials.py then re-auth |
> > 10. | 2 | Vision EXIF+Gemini | PENDING |
> > 11. | 3 | Cross-reference Sheets | PENDING Q2 unresolved |
> > 12. | 4 | WebP Transform | CODE DONE |
> > 13. | 5 | Drive + Notion log | NOTION_DATABASE_ID ready |
> > 14. | 6 | Integration test | PENDING |
> >
> > 15. ---
> >
> > 16. ## Root Cause Log (403 issue)
> > 17. Gemini diagnosis 2026-03-13:
> > 18. - token.json scopes field = client-side "wishlist", NOT server grant
> >     - - Google was reusing old cached refresh_token (no photoslibrary scope)
> >       - - Fix: prompt=consent in flow.run_local_server() forces full consent screen every time
> >           - - Status: fix committed, setup_credentials.py added, pending re-auth test
> >          
> >           - ---
> >
> > ## Open Questions
> > | # | Question | Priority |
> > |---|----------|----------|
> > | Q2 | MAPLAB_Quotes sheet column names + date format? | HIGH |
> > | Q3 | Spouse OAuth done? token_spouse.json exist? | MEDIUM |
> >
> > ---
> >
> > ## Key Config
> > .env (all filled):
> > - MAPLAB_QUOTES_SHEET_ID: 1d2_SiEXh5JT4lzjkgHDI5JU9UWBY9TiPlC8DaxkQnKs
> > - - GOOGLE_DRIVE_ARCHIVE_FOLDER_ID: 1L0udpuXLy3vEbHmzBbaLqNVDut2FFpCe
> >   - - GEMINI_API_KEY: see Notion API Keys page
> >     - - NOTION_TOKEN: see Notion API Keys page
> >       - - NOTION_DATABASE_ID: 320ab0806d5c801b9063d444cd7fbd1c
> >        
> >         - Auth:
> >       - - credentials.json: run `python auth/setup_credentials.py` to auto-copy from Downloads
> >           - - token_owner.json: MISSING - created after re-auth
> >            
> >             - Code:
> >             - - pipeline.py: Phase 1 live
> >               - - collector.py: FIXED (owner-only, timezone.utc, no em-dash)
> >                 - - google_auth.py: FIXED (prompt=consent)
> >                   - - transformer.py: reads .env OK
> >                     - - vision.py / crossref.py / archiver.py: skeletons pending
