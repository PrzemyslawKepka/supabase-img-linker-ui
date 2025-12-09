"""
File handling utilities.
Provides helpers for file operations and sanitization.
"""

import os
from urllib.parse import urlparse


def sanitize_filename(text: str) -> str:
    """
    Sanitize a string to be safe for use as a filename.

    Args:
        text: The text to sanitize

    Returns:
        Sanitized string safe for filenames
    """
    safe_text = "".join([c for c in text if c.isalnum() or c in (" ", "-", "_")])
    return safe_text.strip().replace(" ", "_")


def create_record_filename(record_id: int, title: str, extension: str) -> str:
    """
    Create a standardized filename for record images.

    Args:
        record_id: The record ID
        title: The record title/name
        extension: File extension (should include the dot, e.g., '.jpg')

    Returns:
        Formatted filename: {id}_{sanitized_title}{extension}
    """
    safe_title = sanitize_filename(title)
    return f"{record_id}_{safe_title}{extension}"


def get_extension_from_url(url: str, default: str = ".jpg") -> str:
    """
    Extract file extension from a URL.

    Args:
        url: The URL to extract extension from
        default: Default extension if none can be determined

    Returns:
        File extension including the dot (e.g., '.jpg')
    """
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    return ext if ext else default


def get_content_type(filename: str, default: str = "image/jpeg") -> str:
    """
    Determine content type based on file extension.

    Args:
        filename: The filename or extension (e.g., 'image.png' or '.png')
        default: Default content type if extension is unknown

    Returns:
        MIME type string (e.g., 'image/jpeg')
    """
    # If input is already just an extension (starts with dot), use it directly
    # Otherwise extract extension from filename
    if filename.startswith(".") and "/" not in filename and "\\" not in filename:
        ext = filename.lower()
    else:
        ext = os.path.splitext(filename)[1].lower()

    content_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }

    return content_type_map.get(ext, default)
