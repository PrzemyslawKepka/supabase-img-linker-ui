"""
Image service module.
Handles image upload, URL fetching, and image processing operations.
"""

import requests

from constants.config import ENABLE_IMAGE_OPTIMIZATION, SIGNED_URL_EXPIRY_YEARS
from services.database_service import DatabaseService
from utils.file_helpers import (
    create_record_filename,
    get_content_type,
    get_extension_from_url,
)
from utils.image_optimizer import ImageOptimizer


class ImageService:
    """Service for managing image uploads and URL generation."""

    def __init__(self, db_service: DatabaseService):
        """
        Initialize the image service.

        Args:
            db_service: Database service instance for storage operations
        """
        self.db_service = db_service
        self.optimizer = ImageOptimizer()

    def process_file_upload(
        self, record_id: int, record_title: str, file_data: bytes, filename: str
    ) -> str:
        """
        Process a file upload and return the signed URL.
        Automatically optimizes images before uploading.

        Args:
            record_id: Record ID for the image
            record_title: Record title for filename generation
            file_data: Binary file data
            filename: Original filename

        Returns:
            Signed URL for the uploaded image
        """
        import os

        # Optimize image if enabled
        if ENABLE_IMAGE_OPTIMIZATION:
            try:
                # Get original size for logging
                original_size = len(file_data) / 1024  # KB

                # Optimize the image
                optimized_data, optimized_format = self.optimizer.optimize_image(
                    file_data
                )

                # Calculate compression ratio
                optimized_size = len(optimized_data) / 1024  # KB
                compression_ratio = (1 - optimized_size / original_size) * 100

                # Log optimization results
                import panel as pn

                pn.state.notifications.info(
                    f"Image optimized: {original_size:.1f}KB → {optimized_size:.1f}KB "
                    f"({compression_ratio:.1f}% reduction)",
                    duration=3000,
                )

                # Use optimized data and force JPEG extension
                file_data = optimized_data
                ext = ".jpg"
            except Exception as e:
                # If optimization fails, fall back to original
                import panel as pn

                pn.state.notifications.warning(
                    f"Image optimization failed, using original: {e}", duration=3000
                )
                ext = os.path.splitext(filename)[1].lower()
        else:
            ext = os.path.splitext(filename)[1].lower()

        content_type = get_content_type(ext)

        # Create standardized filename
        new_filename = create_record_filename(record_id, record_title, ext)

        # Upload to storage
        self.db_service.upload_image(file_data, new_filename, content_type)

        # Get signed URL
        signed_url = self._get_signed_url(new_filename)

        # Update database
        self.db_service.update_image_url(record_id, signed_url)

        return signed_url

    def process_url_upload(
        self, record_id: int, record_title: str, image_url: str
    ) -> str:
        """
        Download an image from URL, upload it, and return the signed URL.
        Automatically optimizes images before uploading.

        Args:
            record_id: Record ID for the image
            record_title: Record title for filename generation
            image_url: URL of the image to download

        Returns:
            Signed URL for the uploaded image

        Raises:
            Exception: If download or upload fails
        """
        try:
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = response.content

            # Optimize image if enabled
            if ENABLE_IMAGE_OPTIMIZATION:
                try:
                    # Get original size
                    original_size = len(image_data) / 1024  # KB

                    # Optimize the image
                    optimized_data, optimized_format = self.optimizer.optimize_image(
                        image_data
                    )

                    # Calculate compression ratio
                    optimized_size = len(optimized_data) / 1024  # KB
                    compression_ratio = (1 - optimized_size / original_size) * 100

                    # Log optimization results
                    import panel as pn

                    pn.state.notifications.info(
                        f"Image optimized: {original_size:.1f}KB → {optimized_size:.1f}KB "
                        f"({compression_ratio:.1f}% reduction)",
                        duration=3000,
                    )

                    # Use optimized data and force JPEG
                    image_data = optimized_data
                    ext = ".jpg"
                    content_type = "image/jpeg"
                except Exception as e:
                    # Fall back to original
                    import panel as pn

                    pn.state.notifications.warning(
                        f"Image optimization failed, using original: {e}", duration=3000
                    )
                    ext = get_extension_from_url(image_url)
                    content_type = response.headers.get("Content-Type", "image/jpeg")
            else:
                ext = get_extension_from_url(image_url)
                content_type = response.headers.get("Content-Type", "image/jpeg")

            # Create standardized filename
            new_filename = create_record_filename(record_id, record_title, ext)

            # Upload to storage
            self.db_service.upload_image(image_data, new_filename, content_type)

            # Get signed URL
            signed_url = self._get_signed_url(new_filename)

            # Update database
            self.db_service.update_image_url(record_id, signed_url)

            return signed_url

        except Exception as e:
            raise Exception(f"Failed to download or upload image: {e}")

    def _get_signed_url(self, filename: str) -> str:
        """
        Get a signed URL for a file.

        Args:
            filename: Name of the file in storage

        Returns:
            Signed URL string
        """
        expiry_seconds = 60 * 60 * 24 * 365 * SIGNED_URL_EXPIRY_YEARS
        signed_url_resp = self.db_service.get_signed_url(filename, expiry_seconds)

        # Handle different response formats
        if isinstance(signed_url_resp, dict) and "signedURL" in signed_url_resp:
            return signed_url_resp["signedURL"]
        elif hasattr(signed_url_resp, "signedURL"):
            return signed_url_resp.signedURL
        else:
            return signed_url_resp["signedURL"]
