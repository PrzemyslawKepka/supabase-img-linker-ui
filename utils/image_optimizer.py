"""
Image optimization utility module.
Handles image compression, resizing, and format conversion for optimized storage.
"""

from io import BytesIO
from typing import Tuple

from PIL import Image, ImageOps

from constants.config import (
    IMAGE_MAX_DIMENSION,
    IMAGE_QUALITY,
    THUMBNAIL_MAX_DIMENSION,
    THUMBNAIL_QUALITY,
)


class ImageOptimizer:
    """Service for optimizing images before upload."""

    @staticmethod
    def optimize_image(
        image_data: bytes,
        max_dimension: int = IMAGE_MAX_DIMENSION,
        quality: int = IMAGE_QUALITY,
    ) -> Tuple[bytes, str]:
        """
        Optimize an image by resizing and compressing it.

        Args:
            image_data: Original image data as bytes
            max_dimension: Maximum width or height in pixels
            quality: JPEG quality (1-95, higher = better quality but larger file)

        Returns:
            Tuple of (optimized_image_bytes, format)
        """
        # Open image
        img = Image.open(BytesIO(image_data))

        # Convert RGBA to RGB if necessary (for JPEG compatibility)
        if img.mode in ("RGBA", "LA", "P"):
            # Create a white background
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background

        # Apply EXIF orientation if present
        img = ImageOps.exif_transpose(img)

        # Resize if image is larger than max_dimension
        if max(img.size) > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        # Save optimized image to bytes
        output = BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return output.getvalue(), "jpeg"

    @staticmethod
    def create_thumbnail(
        image_data: bytes,
        max_dimension: int = THUMBNAIL_MAX_DIMENSION,
        quality: int = THUMBNAIL_QUALITY,
    ) -> bytes:
        """
        Create a thumbnail version of an image.

        Args:
            image_data: Original image data as bytes
            max_dimension: Maximum width or height for thumbnail
            quality: JPEG quality for thumbnail

        Returns:
            Thumbnail image bytes
        """
        # Open image
        img = Image.open(BytesIO(image_data))

        # Convert RGBA to RGB if necessary
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

        # Create thumbnail
        img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        # Save to bytes
        output = BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return output.getvalue()

    @staticmethod
    def get_image_info(image_data: bytes) -> dict:
        """
        Get information about an image.

        Args:
            image_data: Image data as bytes

        Returns:
            Dictionary with image information (width, height, format, size)
        """
        img = Image.open(BytesIO(image_data))
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
            "size_bytes": len(image_data),
        }
