"""
Configuration module for Supabase Image Linker UI.
Centralizes all configuration settings and constants.
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "property-images")
DATA_TABLE = "properties_CM_pub"

# Image Validation Configuration
IMAGE_CHECK_TIMEOUT = 3  # seconds
IMAGE_CHECK_MAX_WORKERS = 10

# Image Optimization Configuration
IMAGE_MAX_DIMENSION = 1920  # Max width/height for full images (1920px for HD)
IMAGE_QUALITY = 85  # JPEG quality (1-95, 85 is good balance)
THUMBNAIL_MAX_DIMENSION = 400  # Max dimension for thumbnails
THUMBNAIL_QUALITY = 75  # Lower quality for thumbnails (smaller file size)
ENABLE_IMAGE_OPTIMIZATION = True  # Enable/disable image optimization

# UI Configuration
TABLE_PAGE_SIZE = 20
IMAGE_PREVIEW_WIDTH = 300
IMAGE_PREVIEW_HEIGHT = 200
ACCEPTED_IMAGE_FORMATS = ".jpg,.jpeg,.png,.webp"

# URL Signing Configuration
SIGNED_URL_EXPIRY_YEARS = 10

# Status Filter Options
STATUS_FILTER_OPTIONS = ["All", "OK", "Error"]
STATUS_FILTER_DEFAULT = "All"

# Upload Type Options
UPLOAD_TYPE_OPTIONS = ["Upload File", "Image URL"]
UPLOAD_TYPE_DEFAULT = "Upload File"

# Theme Configuration
HEADER_BACKGROUND_COLOR = "#3A7D7E"
