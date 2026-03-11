"""
Image Transformer Module
Converts photos to WebP format with SEO-optimized filenames.

Phase: 4
Status: SKELETON

Output filename pattern:
    {YYYYMMDD}_{project_name_slug}_{kw1-kw2-kw3}.webp
    
Example:
    20260310_tainan-wedding-catering_milkfish-panfry-taiwanese.webp
"""

import re
import logging
from pathlib import Path
from PIL import Image

logger = logging.getLogger('maplab.transformer')

# WebP settings
WEBP_QUALITY = 80
MAX_WIDTH = 2000
OUTPUT_DIR = Path("./output")


def slugify(text: str, max_len: int = 30) -> str:
    """Convert text to URL/filename safe lowercase slug."""
    text = str(text).lower().strip()
    # Remove non-alphanumeric except spaces/hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:max_len].strip('-')


def build_filename(
    captured_at,
    project_name: str,
    keywords: list
) -> str:
    """
    Build SEO-optimized WebP filename.
    
    Args:
        captured_at: datetime object
        project_name: From crossref (e.g. "tainan-wedding")
        keywords: From Gemini (e.g. ["milkfish", "panfry", "taiwanese"])
    
    Returns:
        Filename without path, e.g. "20260310_tainan-wedding_milkfish-panfry-taiwanese.webp"
    """
    date_str = captured_at.strftime("%Y%m%d")
    
    project_slug = slugify(project_name, max_len=30) if project_name else "maplab"
    
    # Take up to 3 keywords
    kw_slug = '-'.join(slugify(kw, max_len=20) for kw in keywords[:3])
    
    filename = f"{date_str}_{project_slug}_{kw_slug}.webp"
    
    # Ensure total length is reasonable
    if len(filename) > 80:
        # Truncate project slug to fit
        filename = f"{date_str}_{project_slug[:15]}_{kw_slug}.webp"
    
    return filename


def transform_photo(
    photo_record,
    project_info: dict,
    vision_result: dict,
    output_dir: Path = None
) -> dict:
    """
    Transform photo to WebP with SEO filename.
    
    Returns:
        {
            "output_path": str,
            "filename": str,
            "original_size_kb": int,
            "output_size_kb": int,
            "compression_ratio": float
        }
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build filename
    filename = build_filename(
        captured_at=photo_record.captured_at,
        project_name=project_info.get("project_name", "maplab"),
        keywords=vision_result.get("keywords", ["photo"])
    )
    
    output_path = output_dir / filename
    
    # Handle filename collision
    if output_path.exists():
        stem = output_path.stem
        output_path = output_dir / f"{stem}_2.webp"
    
    # Process image
    original_size = Path(photo_record.local_path).stat().st_size
    
    img = Image.open(photo_record.local_path)
    
    # Convert HEIC/CMYK to RGB
    if img.mode in ("CMYK", "P", "RGBA"):
        img = img.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")
    
    # Resize if wider than MAX_WIDTH
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        new_height = int(img.height * ratio)
        img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)
        logger.debug(f"Resized: {img.width}x{img.height}")
    
    # Strip EXIF (privacy — remove GPS data)
    # Note: Pillow WebP save doesn't preserve EXIF by default
    # We explicitly do NOT pass exif= parameter
    
    img.save(str(output_path), format="WEBP", quality=WEBP_QUALITY, method=6)
    
    output_size = output_path.stat().st_size
    compression_ratio = round(original_size / output_size, 2) if output_size > 0 else 0
    
    logger.info(
        f"Transformed: {filename} | "
        f"{original_size//1024}KB → {output_size//1024}KB | "
        f"ratio: {compression_ratio}x"
    )
    
    return {
        "output_path": str(output_path),
        "filename": filename,
        "original_size_kb": original_size // 1024,
        "output_size_kb": output_size // 1024,
        "compression_ratio": compression_ratio
    }
