"""
Batch optimization script for existing images in Supabase.
This script downloads all existing images, optimizes them, and re-uploads them.

Usage:
    python scripts/optimize_existing_images.py [--dry-run] [--limit N]

Options:
    --dry-run: Preview what would be optimized without making changes
    --limit N: Only process first N images (for testing)
"""

import argparse
import sys
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from PIL import Image, ImageOps
from supabase import Client, create_client

# Add parent directory to path to import from constants
sys.path.insert(0, str(Path(__file__).parent.parent))

from constants.config import (
    DATA_TABLE,
    ENTITY_LABEL,
    ENTITY_LABEL_PLURAL,
    ID_COLUMN,
    IMAGE_MAX_DIMENSION,
    IMAGE_QUALITY,
    IMAGE_URL_COLUMN,
    SIGNED_URL_EXPIRY_YEARS,
    STORAGE_BUCKET,
    SUPABASE_KEY,
    SUPABASE_URL,
    TITLE_COLUMN,
)
from utils.file_helpers import create_record_filename

# Load environment variables
load_dotenv()


class SimpleImageOptimizer:
    """Standalone image optimizer using configuration from constants."""

    @staticmethod
    def optimize_image(
        image_data: bytes,
        max_dimension: int = IMAGE_MAX_DIMENSION,
        quality: int = IMAGE_QUALITY,
    ):
        """Optimize an image."""
        img = Image.open(BytesIO(image_data))

        # Convert RGBA to RGB
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background

        # Apply EXIF orientation
        img = ImageOps.exif_transpose(img)

        # Resize if needed
        if max(img.size) > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        # Save optimized
        output = BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return output.getvalue(), "jpeg"

    @staticmethod
    def get_image_info(image_data: bytes):
        """Get image information."""
        img = Image.open(BytesIO(image_data))
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
            "size_bytes": len(image_data),
        }


def optimize_existing_images(dry_run: bool = False, limit: int = None):
    """Optimize all existing images in Supabase."""
    print("=" * 60)
    print("Supabase Image Batch Optimization Script")
    print("=" * 60)

    if dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made\n")

    # Initialize Supabase client
    print("Initializing Supabase connection...")

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        return

    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    optimizer = SimpleImageOptimizer()

    # Fetch all records
    print(f"Fetching {ENTITY_LABEL_PLURAL.lower()} from database...")
    response = client.table(DATA_TABLE).select("*").execute()
    df = pd.DataFrame(response.data)
    print(f"Found {len(df)} total {ENTITY_LABEL_PLURAL.lower()}")

    # Filter only records with image URLs and valid titles
    df_with_images = df[
        df[IMAGE_URL_COLUMN].notna()
        & (df[IMAGE_URL_COLUMN] != "")
        & df[TITLE_COLUMN].notna()
        & (df[TITLE_COLUMN] != "")
    ]
    print(
        f"Found {len(df_with_images)} {ENTITY_LABEL_PLURAL.lower()} with images and valid titles"
    )

    if limit:
        df_with_images = df_with_images.head(limit)
        print(f"Processing only first {limit} images (--limit flag)")

    # Process each image
    total = len(df_with_images)
    optimized_count = 0
    failed_count = 0
    total_original_size = 0
    total_optimized_size = 0

    print("\n" + "=" * 60)
    print("Starting optimization process...")
    print("=" * 60 + "\n")

    for idx, (_, row) in enumerate(df_with_images.iterrows(), 1):
        record_id = row[ID_COLUMN]
        record_title = row[TITLE_COLUMN]
        image_url = row[IMAGE_URL_COLUMN]

        print(f"[{idx}/{total}] Processing {ENTITY_LABEL} ID: {record_id}")
        print(f"  Title: {record_title}")
        print(f"  Current URL: {image_url[:80]}...")

        try:
            # Download current image
            print("  → Downloading image...")
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            original_data = response.content
            original_size_kb = len(original_data) / 1024

            # Get image info
            img_info = optimizer.get_image_info(original_data)
            print(
                f"  → Original: {img_info['width']}x{img_info['height']} "
                f"{img_info['format']}, {original_size_kb:.1f}KB"
            )

            # Optimize image
            print("  → Optimizing...")
            optimized_data, optimized_format = optimizer.optimize_image(original_data)
            optimized_size_kb = len(optimized_data) / 1024
            compression_ratio = (1 - optimized_size_kb / original_size_kb) * 100

            print(
                f"  → Optimized: {optimized_size_kb:.1f}KB "
                f"({compression_ratio:.1f}% reduction)"
            )

            # Skip if optimization didn't help much (< 10% reduction)
            if compression_ratio < 10:
                print("  ⚠ Skipping: Less than 10% size reduction")
                continue

            if not dry_run:
                # Upload optimized image
                print("  → Uploading optimized image...")
                filename = create_record_filename(record_id, record_title, ".jpg")
                bucket = client.storage.from_(STORAGE_BUCKET)
                bucket.upload(
                    path=filename,
                    file=optimized_data,
                    file_options={"content-type": "image/jpeg", "upsert": "true"},
                )

                # Get new signed URL
                expiry_seconds = 60 * 60 * 24 * 365 * SIGNED_URL_EXPIRY_YEARS
                signed_url_resp = bucket.create_signed_url(filename, expiry_seconds)
                if isinstance(signed_url_resp, dict) and "signedURL" in signed_url_resp:
                    new_signed_url = signed_url_resp["signedURL"]
                else:
                    new_signed_url = signed_url_resp.signedURL

                # Update database
                client.table(DATA_TABLE).update({IMAGE_URL_COLUMN: new_signed_url}).eq(
                    ID_COLUMN, record_id
                ).execute()
                print("  ✅ Successfully optimized and uploaded!")
            else:
                print("  ✅ Would optimize and upload (dry-run)")

            optimized_count += 1
            total_original_size += original_size_kb
            total_optimized_size += optimized_size_kb

        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed_count += 1

        print()  # Blank line between records

    # Print summary
    print("=" * 60)
    print("OPTIMIZATION SUMMARY")
    print("=" * 60)
    print(f"Total {ENTITY_LABEL_PLURAL.lower()} processed: {total}")
    print(f"Successfully optimized: {optimized_count}")
    print(f"Failed: {failed_count}")
    print(f"Skipped (already optimal): {total - optimized_count - failed_count}")

    if optimized_count > 0:
        total_compression = (
            (1 - total_optimized_size / total_original_size) * 100
            if total_original_size > 0
            else 0
        )
        print("\nTotal size reduction:")
        print(f"  Before: {total_original_size:.1f}KB")
        print(f"  After: {total_optimized_size:.1f}KB")
        print(f"  Saved: {total_original_size - total_optimized_size:.1f}KB")
        print(f"  Compression: {total_compression:.1f}%")

    if dry_run:
        print("\n🔍 This was a DRY RUN - no changes were made")
        print("Run without --dry-run to apply optimizations")

    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch optimize existing images in Supabase"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be optimized without making changes",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Only process first N images"
    )

    args = parser.parse_args()

    try:
        optimize_existing_images(dry_run=args.dry_run, limit=args.limit)
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
