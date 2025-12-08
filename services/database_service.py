"""
Database service module.
Handles all interactions with Supabase database and storage.
"""

import pandas as pd
from supabase import Client, create_client

from constants.config import (
    DATA_TABLE,
    ID_COLUMN,
    IMAGE_URL_COLUMN,
    STORAGE_BUCKET,
    SUPABASE_KEY,
    SUPABASE_URL,
)


class DatabaseService:
    """Service for managing Supabase database and storage operations."""

    def __init__(self):
        """Initialize the database service with Supabase client."""
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not found in environment variables.")

        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.client: Client = create_client(self.url, self.key)
        self.data_table = DATA_TABLE
        self.bucket_name = STORAGE_BUCKET
        self.id_column = ID_COLUMN
        self.image_url_column = IMAGE_URL_COLUMN

    def fetch_records(self) -> pd.DataFrame:
        """
        Fetch all records from the configured database table.

        Returns:
            DataFrame containing all records
        """
        response = self.client.table(self.data_table).select("*").execute()
        return pd.DataFrame(response.data)

    def update_image_url(self, record_id: int, image_url: str) -> None:
        """
        Update the image URL for a specific record.

        Args:
            record_id: The record ID to update
            image_url: The new image URL
        """
        self.client.table(self.data_table).update(
            {self.image_url_column: image_url}
        ).eq(self.id_column, record_id).execute()

    def upload_image(
        self, file_data: bytes, file_name: str, content_type: str = "image/jpeg"
    ):
        """
        Upload an image to Supabase Storage.

        Args:
            file_data: Image file data as bytes
            file_name: Destination path in the bucket (e.g., "property_123.jpg")
            content_type: MIME type of the image

        Returns:
            Upload response from Supabase
        """
        bucket = self.client.storage.from_(self.bucket_name)
        response = bucket.upload(
            path=file_name,
            file=file_data,
            file_options={"content-type": content_type, "upsert": "true"},
        )
        return response

    def get_signed_url(self, file_path: str, expiry_seconds: int):
        """
        Generate a signed URL for a file in storage.

        Args:
            file_path: Path to the file in the bucket
            expiry_seconds: Expiry time in seconds

        Returns:
            Dict containing the signed URL
        """
        return self.client.storage.from_(self.bucket_name).create_signed_url(
            file_path, expiry_seconds
        )
