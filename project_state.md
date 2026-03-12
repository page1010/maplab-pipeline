⚡工作規則（給所有協作者）：每次工作前先讀此檔案翻閱監控面板與各模組→完成後更新此檔案→限制前寫下。只跑不需要人工操作的區塊，切割小步驟，每步驟獨立。🚫絕對禁止規則：任何情況下都不得刪除原始相片。只做「讀取→轉換副本→上傳副本→記錄」，原始檔案永遠保持不動。🗓️—🎯→原始相片永不刪除。✅→保管室———🔄→⏭️→→✅→🚫—→→→—保管室📋✅🔧—⏳⏳—✅✅⏳❓——🧠✅✅✅保管室✅保管室✅✅❓✅🔧—✅✅—✅✅📁├──├──←├──├──├──│├──││├──✅—││├──✅││└──❓│├──🔧—│├──✅│├──✅│├──✅│├──✅│└──✅├──│└──├──│├──│└──└──├──✅└──✅# PROJECT STATE
⚡ AI Collaborator: Read this file FIRST. Update this file LAST.
This is the single source of truth for all AI handoffs.

> **工作規則（給所有 AI 協作者）**：每次工作前先讀此檔案 + 翻閱 Notion 監控面板與 GitHub 各模組 → 完成後更新此檔案 → Token 限制前寫下 Next Task。只跑不需要人工操作的區塊，切割小步驟，每步驟獨立 commit。
>
> > **🚫 絕對禁止規則**：任何情況下都不得刪除原始相片。pipeline 只做「讀取 → 轉換副本 → 上傳副本 → 記錄」，原始檔案永遠保持不動。
> >
> > ---
> >
> > ## 🗓️ Last Updated
> > - **Date**: 2026-03-12
> > - - **Updated by**: Claude (Sonnet 4.6)
> >   - - **Session type**: Block 3.3 — Phase 1 collector uncommented, pipeline live
> >     - 
---

## 🎯 Project Goal (One Line)
Build a Python pipeline that auto-processes MAPLAB photos → WebP assets with SEO names, cross-referenced with catering quotes and travel itineraries, logged to Notion. **原始相片永不刪除。**

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
| 2.4 | Notion checklist: ticked GCP, credentials.json, .env filled | Claude | 2026-03-11 |
| 2.5 | Notion: API Keys 保管室 page created — all keys archived | Claude | 2026-03-11 |
| 2.6 | NOTION_TOKEN obtained from Internal integration | Claude | 2026-03-11 |
| 2.7 | ASSET_LOG Notion DB created — 10 columns matching archiver.py schema | Claude | 2026-03-12 |
| 2.8 | NOTION_DATABASE_ID confirmed: 320ab0806d5c801b9063d444cd7fbd1c | Claude | 2026-03-12 |
| 2.9 | No-delete rule added to project_state.md and Notion | Claude | 2026-03-12 |
| 3.1 | OAuth complete: owner token valid (token_owner.json confirmed) | Human | 2026-03-12 |
| 3.2 | pip install -r requirements.txt complete | Human | 2026-03-12 |
| 3.3 | pipeline.py Phase 1 collector uncommented — live run enabled | Claude | 2026-03-12 |

---

## 🔄 Current Task
**Phase 1 collector is now LIVE in pipeline.py.**

Next step requires human to run locally and paste output:
```
cd maplab-pipeline
python src/pipeline.py --test
```
Then paste the output here so AI can check for errors.

---

## ⏭️ Next Task (for next AI session)
1. Human runs: `python src/pipeline.py --test` and pastes output
2. 2. AI reads output → fixes any import/API errors → commits fix
   3. 3. If test passes: tick Phase 1 complete in Notion, update roadmap
      4. 4. Then: implement Phase 2 crossref (needs Q2 resolved: Sheets column names)
        
         5. ---
        
         6. ## 🚫 SAFETY RULES (NON-NEGOTIABLE)
         7. 1. **NEVER delete original photos** — pipeline reads → converts copy → uploads copy → logs. Source files untouched.
            2. 2. **NEVER commit .env** — it's gitignored, contains secrets
               3. 3. **NEVER share API Keys 保管室 URL** publicly
                 
                  4. ---
                 
                  5. ## 📋 Full Phase Roadmap
                  6. | Phase | Description | Status |
                  7. |-------|-------------|--------|
                  8. | 0 | Scaffolding | ✅ DONE |
                  9. | 1 | OAuth + Collector | ✅ LIVE — collector uncommented, awaiting --test run |
                  10. | 2 | Vision (EXIF+Gemini) | ⏳ PENDING |
                  11. | 3 | Cross-reference (Sheets + Calendar) | ⏳ PENDING — Q2 unresolved |
                  12. | 4 | WebP Transform | ✅ CODE COMPLETE |
                  13. | 5 | Drive + Notion log | ✅ NOTION_DATABASE_ID ready |
                  14. | 6 | Integration test | ⏳ PENDING |
                 
                  15. ---
                 
                  16. ## ❓ Open Questions
                  17. | # | Question | Priority | Notes |
                  18. |---|----------|----------|-------|
                  19. | Q1 | Google account type: Personal or Workspace? | HIGH | Affects OAuth consent screen |
                  20. | Q2 | MAPLAB_Quotes sheet — exact column names? Date format (YYYY/MM/DD or MM/DD?)? | HIGH | Needed for Phase 3 crossref.py |
                  21. | Q3 | Spouse OAuth done? token_spouse.json exist? | MEDIUM | Confirm before running --accounts spouse |
                  22. | Q4 | Spouse's Google account — same OAuth app or separate credentials? | MEDIUM | Affects collector design |
                 
                  23. ---
                 
                  24. ## 🧠 Context for Next AI
                  25. **Current .env status (ALL COMPLETE):**
                  26. - MAPLAB_QUOTES_SHEET_ID: ✅ 1d2_SiEXh5JT4lzjkgHDI5JU9UWBY9TiPlC8DaxkQnKs
                      - - GOOGLE_DRIVE_ARCHIVE_FOLDER_ID: ✅ 1L0udpuXLy3vEbHmzBbaLqNVDut2FFpCe
                        - - GEMINI_API_KEY: ✅ (see Notion API Keys 保管室)
                          - - NOTION_TOKEN: ✅ (see Notion API Keys 保管室)
                            - - NOTION_DATABASE_ID: ✅ 320ab0806d5c801b9063d444cd7fbd1c
                             
                              - **Auth status:**
                              - - token_owner.json: ✅ exists and valid (confirmed 2026-03-12)
                                - - token_spouse.json: ❓ not confirmed yet
                                 
                                  - **Notion API Keys 保管室:** https://www.notion.so/API-Keys-maplab-pipeline-320ab0806d5c80e0be95f298399d2c44
                                 
                                  - **ASSET_LOG Database:**
                                  - - URL: https://www.notion.so/320ab0806d5c801b9063d444cd7fbd1c
                                    - - Columns: Name(title), Date(date), Category(select), Project Name(rich_text), Drive Link(url), AI Keywords(multi_select), Alt Text(rich_text), Status(select), Original Filename(rich_text), Output Size KB(number)
                                     
                                      - **Code status (v1.9):**
                                      - - pipeline.py: ✅ Phase 1 collector LIVE (uncommented 2026-03-12)
                                        - - transformer.py: ✅ reads .env
                                          - - collector.py: ✅ complete, auth working
                                            - - vision.py: ✅ complete skeleton — Phase 2 TODO
                                              - - crossref.py: ✅ skeleton, Q2 TBD — Phase 3 TODO
                                                - - archiver.py: ✅ skeleton, NOTION_DATABASE_ID confirmed — Phase 5 TODO
                                                 
                                                  - ---

                                                  ## 📁 Repository File Map
                                                  ```
                                                  maplab-pipeline/
                                                  ├── README.md
                                                  ├── project_state.md        ← YOU ARE HERE
                                                  ├── .env.example
                                                  ├── requirements.txt
                                                  ├── src/
                                                  │   ├── auth/
                                                  │   │   ├── google_auth.py  ✅ OAuth working — token_owner.json confirmed
                                                  │   │   ├── token_owner.json ✅ (local only, gitignored)
                                                  │   │   └── token_spouse.json ❓ (not confirmed)
                                                  │   ├── collector.py        ✅ ready & called in pipeline.py
                                                  │   ├── vision.py           ✅ Gemini 1.5 Flash skeleton
                                                  │   ├── crossref.py         ✅ skeleton, Q2 TBD
                                                  │   ├── transformer.py      ✅ reads .env
                                                  │   ├── archiver.py         ✅ NOTION_DATABASE_ID confirmed
                                                  │   └── pipeline.py         ✅ Phase 1 LIVE (collector uncommented)
                                                  ├── docs/
                                                  │   └── naming_rules.md
                                                  ├── schemas/
                                                  │   ├── notion_entry.schema.json
                                                  │   └── photo_record.schema.json
                                                  └── tests/
                                                      ├── test_date_tolerance.py ✅
                                                      └── test_transformer.py    ✅
                                                  ```

                                                  Always update this file at the end of your session.
