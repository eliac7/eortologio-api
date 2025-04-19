"""HTTP utilities for making external requests."""

import requests
from fastapi import HTTPException
from app.core.config import logger


def make_request(url: str) -> requests.Response:
    """
    Helper function to make requests with user agent and timeout.

    Args:
        url: The URL to request

    Returns:
        Response object

    Raises:
        HTTPException: When request fails or times out
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching URL {url}")
        raise HTTPException(
            status_code=504,
            detail="Request timed out while fetching data from eortologio.net.",
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        raise HTTPException(
            status_code=503, detail=f"Could not fetch data from eortologio.net: {e}"
        )
