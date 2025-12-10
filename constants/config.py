"""
Configuration module for Supabase Image Linker UI.
Centralizes all configuration settings and constants.

This file defines the table and column mappings for the application.
Customize these settings to work with any Supabase table structure.
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "property-images")

# ==============================================================================
# TABLE CONFIGURATION - CUSTOMIZE FOR YOUR USE CASE
# ==============================================================================

# Table name in Supabase
DATA_TABLE = "properties_CM_pub"

# Column name for the unique identifier (e.g., "id", "user_id", "product_id")
ID_COLUMN = "id"

# Column name for the image URL field (e.g., "image_url", "avatar_url", "photo_url")
IMAGE_URL_COLUMN = "image_url"

# Column name for a descriptive title/name field (e.g., "title", "name", "username")
TITLE_COLUMN = "title"

# Additional columns to display in the table (optional)
# These will be shown in the info panel when a row is selected
# Example: ["description", "price", "category"] or ["email", "full_name"]
ADDITIONAL_DISPLAY_COLUMNS = ["listing_url"]

# Label for the entity being managed (e.g., "Property", "User", "Product")
# This will be used in UI labels and messages
ENTITY_LABEL = "Property"
ENTITY_LABEL_PLURAL = "Properties"

# Image Validation Configuration
IMAGE_CHECK_TIMEOUT = 3  # seconds (for HEAD requests to validate URLs)
IMAGE_CHECK_MAX_WORKERS = 10

# Image Download Configuration
IMAGE_DOWNLOAD_TIMEOUT = 10  # seconds (for downloading full images from URLs)

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
