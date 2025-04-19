"""Application configuration settings."""

import logging
from typing import Dict

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URL for the eortologio.net website
BASE_URL = "https://www.eortologio.net"

# Cache duration in seconds (6 hours)
CACHE_DURATION_SECONDS = 6 * 60 * 60

# Greek month names mapping (genitive case to number)
MONTH_NAMES_GREEK_GENITIVE: Dict[str, int] = {
    "Ιανουαρίου": 1,
    "Φεβρουαρίου": 2,
    "Μαρτίου": 3,
    "Απριλίου": 4,
    "Μαΐου": 5,
    "Ιουνίου": 6,
    "Ιουλίου": 7,
    "Αυγούστου": 8,
    "Σεπτεμβρίου": 9,
    "Οκτωβρίου": 10,
    "Νοεμβρίου": 11,
    "Δεκεμβρίου": 12,
}

# Greek month names mapping (number to nominative case)
MONTH_NAMES_GREEK_NOMINATIVE: Dict[int, str] = {
    1: "Ιανουάριος",
    2: "Φεβρουάριος",
    3: "Μάρτιος",
    4: "Απρίλιος",
    5: "Μάιος",
    6: "Ιούνιος",
    7: "Ιούλιος",
    8: "Αύγουστος",
    9: "Σεπτέμβριος",
    10: "Οκτώβριος",
    11: "Νοέμβριος",
    12: "Δεκέμβριος",
}
