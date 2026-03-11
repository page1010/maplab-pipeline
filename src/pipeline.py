"""
MAPLAB Digital Asset Pipeline v2.0
Main orchestrator — runs all modules in sequence.

Usage:
    python pipeline.py                    # Process new photos since last run
    python pipeline.py --test             # Test mode: process 1 photo only
    python pipeline.py --phase 1          # Run specific phase only
    python pipeline.py --date 2026-03-10  # Process photos from specific date

AI Collaborator Note:
    See project_state.md for current development phase.
    Each module has its own file in src/.
"""

import logging
import argparse
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('maplab.pipeline')

STATE_FILE = Path('state/pipeline_state.json')


def load_state() -> dict:
    """Load pipeline state from disk. Creates default state if not found."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "last_run": None,
        "processed_ids": [],
        "failed_ids": [],
        "stats": {"total_processed": 0, "catering": 0, "travel": 0, "other": 0}
    }


def save_state(state: dict):
    """Persist pipeline state to disk."""
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, default=str)
    logger.info(f"State saved: {state['stats']}")


def run_pipeline(test_mode: bool = False, target_date: str = None):
    """
    Main pipeline execution.
    
    TODO (Phase 6): Wire all modules together.
    Currently each module is a stub — implement in order (Phase 1 → 5).
    """
    logger.info("=" * 60)
    logger.info("MAPLAB Pipeline starting")
    logger.info(f"Test mode: {test_mode} | Target date: {target_date}")
    
    state = load_state()
    
    # ─── Phase 1: Collect ────────────────────────────────────────
    logger.info("[Phase 1] Collecting photos from Google Photos...")
    # from src.collector import collect_photos
    # photos = collect_photos(
    #     since=state['last_run'],
    #     processed_ids=state['processed_ids'],
    #     limit=1 if test_mode else None,
    #     target_date=target_date
    # )
    # logger.info(f"Collected {len(photos)} new photos")
    photos = []  # TODO: replace with actual collector

    if not photos:
        logger.info("No new photos to process. Exiting.")
        return

    results = []
    
    for photo in photos:
        logger.info(f"Processing: {photo.original_filename}")
        
        try:
            # ─── Phase 2: Cross-reference ────────────────────────────
            # from src.crossref import resolve_project
            # project_info = resolve_project(photo.captured_at)
            project_info = {"project_name": "unknown", "category": "other"}  # TODO
            
            # ─── Phase 3: Vision (EXIF + Gemini) ────────────────────
            # from src.vision import analyze_photo
            # vision_result = analyze_photo(photo, project_info)
            vision_result = {"keywords": [], "alt_text": "", "category": "other"}  # TODO
            
            # ─── Phase 4: Transform ──────────────────────────────────
            # from src.transformer import transform_photo
            # transformed = transform_photo(photo, project_info, vision_result)
            transformed = None  # TODO
            
            # ─── Phase 5: Archive ────────────────────────────────────
            # from src.archiver import archive_photo, log_to_notion
            # drive_url = archive_photo(transformed)
            # log_to_notion(photo, project_info, vision_result, drive_url)
            
            state['processed_ids'].append(photo.photo_id)
            state['stats']['total_processed'] += 1
            state['stats'][vision_result['category']] = \
                state['stats'].get(vision_result['category'], 0) + 1
            
            logger.info(f"✓ Processed: {photo.original_filename}")
            
        except Exception as e:
            logger.error(f"✗ Failed: {photo.original_filename} — {e}")
            state['failed_ids'].append(photo.photo_id)
    
    state['last_run'] = datetime.utcnow().isoformat()
    save_state(state)
    
    logger.info("=" * 60)
    logger.info(f"Pipeline complete. Stats: {state['stats']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MAPLAB Digital Asset Pipeline')
    parser.add_argument('--test', action='store_true', help='Process 1 photo only')
    parser.add_argument('--phase', type=int, help='Run specific phase (1-5)')
    parser.add_argument('--date', type=str, help='Target date YYYY-MM-DD')
    args = parser.parse_args()
    
    run_pipeline(test_mode=args.test, target_date=args.date)
