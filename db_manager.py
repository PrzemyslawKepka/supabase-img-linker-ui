import os

import pandas as pd
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "property-images")
DATA_TABLE = "properties_CM_pub"


class Database:
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not found in environment variables.")

        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.client: Client = create_client(self.url, self.key)
        self.data_table = DATA_TABLE
        self.bucket_name = STORAGE_BUCKET

    def fetch_properties(self) -> pd.DataFrame:
        """Fetch all properties from the database."""
        response = self.client.table(self.data_table).select("*").execute()
        df = pd.DataFrame(response.data)
        return df

    def update_image_url(self, property_id, image_url):
        """Update the image_url for a specific property."""
        # We use 'id' as the identifier.
        self.client.table(self.data_table).update({"image_url": image_url}).eq(
            "id", property_id
        ).execute()

    def upload_image(self, file_obj, file_name, content_type="image/jpeg"):
        """
        Upload an image to Supabase Storage.
        file_obj: bytes or file-like object
        file_name: destination path in the bucket (e.g., "property_123.jpg")
        """
        bucket = self.client.storage.from_(self.bucket_name)
        # We try to upload. If it exists, we might want to overwrite or handle it.
        # upsert='true' allows overwriting.
        response = bucket.upload(
            path=file_name,
            file=file_obj,
            file_options={"content-type": content_type, "upsert": "true"},
        )
        return response

    def get_signed_url(self, file_path, years=10):
        """Generate a signed URL for the file."""
        expiry = 60 * 60 * 24 * 365 * years
        return self.client.storage.from_(self.bucket_name).create_signed_url(
            file_path, expiry
        )
