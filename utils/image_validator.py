"""
Image validation utilities.
Handles checking image URL availability and status.
"""

from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from constants.config import IMAGE_CHECK_MAX_WORKERS, IMAGE_CHECK_TIMEOUT


def get_image_status(url: str) -> bool:
    """
    Check if an image URL is accessible and returns a valid response.

    Args:
        url: The image URL to check

    Returns:
        True if image is accessible (HTTP 200), False otherwise
    """
    if not url or pd.isna(url) or url == "":
        return False

    try:
        response = requests.head(url, timeout=IMAGE_CHECK_TIMEOUT)
        return response.status_code == 200
    except Exception:
        return False


def check_images_parallel(urls: list) -> list:
    """
    Check multiple image URLs in parallel for better performance.

    Args:
        urls: List of image URLs to check

    Returns:
        List of boolean status results (True=OK, False=Error)
    """
    with ThreadPoolExecutor(max_workers=IMAGE_CHECK_MAX_WORKERS) as executor:
        results = list(executor.map(get_image_status, urls))
    return results
