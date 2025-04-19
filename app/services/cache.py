"""Caching services for API data."""

from cachetools import TTLCache
from app.core.config import CACHE_DURATION_SECONDS

# TTLCache for monthly data (12 months max)
monthly_data_cache = TTLCache(maxsize=12, ttl=CACHE_DURATION_SECONDS)

# TTLCache for name search results (200 names max)
name_search_cache = TTLCache(maxsize=200, ttl=CACHE_DURATION_SECONDS)
