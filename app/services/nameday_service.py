"""Services for fetching and parsing nameday data."""

from typing import List, Dict, Any
import urllib.parse
import re
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from fastapi import HTTPException
from cachetools import cached

from app.utils.http import make_request
from app.services.cache import monthly_data_cache, name_search_cache
from app.core.config import (
    BASE_URL,
    MONTH_NAMES_GREEK_GENITIVE,
    MONTH_NAMES_GREEK_NOMINATIVE,
    logger,
)


@cached(monthly_data_cache)
def fetch_and_parse_month_data(month: int) -> List[Dict[str, Any]]:
    """
    Fetches and parses the nameday data for a specific month from eortologio.net.

    Args:
        month: Month number (1-12)

    Returns:
        List of nameday entries for the month

    Raises:
        ValueError: If month number is invalid
        HTTPException: If parsing fails
    """
    if month not in MONTH_NAMES_GREEK_NOMINATIVE:
        raise ValueError("Invalid month number")

    month_name = MONTH_NAMES_GREEK_NOMINATIVE[month]
    # URL encode the month name properly
    encoded_month_name = urllib.parse.quote(month_name)
    url = f"{BASE_URL}/month/{month}/{encoded_month_name}"
    logger.info(f"Fetching monthly data for month {month} from {url}")

    response = make_request(url)
    soup = BeautifulSoup(response.text, "lxml")

    data_table = soup.find("table", id="table0")
    if not data_table:
        logger.error(f"Could not find data table with id='table0' on {url}")
        raise HTTPException(
            status_code=500, detail="Could not parse data table from eortologio.net."
        )

    month_data = []
    tbody = data_table.find("tbody")
    if not tbody:
        logger.warning(f"No tbody found in table0 for month {month}")
        return []

    rows = tbody.find_all("tr", class_="row", recursive=False)

    for row in rows:
        cells = row.find_all("td", recursive=False)
        if len(cells) != 4:
            continue

        # --- Extract Day ---
        day_cell = cells[0]
        day_str = day_cell.get("name")
        if not day_str or not day_str.isdigit():
            day_link = day_cell.find("a")
            if day_link and day_link.text.strip().isdigit():
                day_str = day_link.text.strip()
            else:
                logger.warning(
                    f"Could not extract day number from row in month {month}: {row.prettify()}"
                )
                continue
        try:
            day = int(day_str)
        except (ValueError, TypeError):
            logger.warning(f"Invalid day number format '{day_str}' in month {month}")
            continue

        # --- Extract Names ---
        names_cell = cells[2]
        names_list = []
        name_divs = names_cell.find_all("div", class_="name")
        for div in name_divs:
            name_links = div.find_all("a")
            for link in name_links:
                name = link.text.strip()
                if name:
                    names_list.append(name)
        names_list = list(dict.fromkeys(names_list))

        # --- Check for other celebration dates indicator (*) ---
        has_other_dates_flags = []
        for div in name_divs:
            name_links = div.find_all("a")
            for link in name_links:
                following_text = link.next_sibling
                if (
                    following_text
                    and isinstance(following_text, str)
                    and "*" in following_text
                ):
                    name_text = link.text.strip()
                    if name_text:
                        has_other_dates_flags.append(name_text)
        has_other_dates_flags = list(dict.fromkeys(has_other_dates_flags))

        # --- Extract Saints/Feasts ---
        saints_cell = cells[3]
        saints_list = []
        # Find bold text (often main feasts) and links (specific saints/feasts)
        important_items = saints_cell.find_all(["b", "a"])
        if not important_items:
            saint_text = saints_cell.get_text(separator=" ", strip=True)
            saint_text = re.sub(
                r"\s*\(.*?\)\s*", "", saint_text
            ).strip()  # Remove text in parentheses
            if saint_text:
                saints_list.append(saint_text)
        else:
            for item in important_items:
                text = item.get_text(strip=True)
                if text:
                    saints_list.append(text)
        saints_list = list(dict.fromkeys(saints_list))  # Remove duplicates

        # --- Extract Other Info (World Days, etc.) ---
        other_info = []
        # Check both names_cell and saints_cell for span.whats
        for cell in [names_cell, saints_cell]:
            info_span = cell.find("span", class_="whats")
            if info_span:
                # Iterate through contents to handle <br> better
                for content in info_span.contents:
                    if isinstance(content, Tag) and content.name == "br":
                        continue
                    text = content.get_text(strip=True)
                    if text:
                        other_info.append(text)
                break  # Assume only one relevant span.whats per row

        month_data.append(
            {
                "day": day,
                "month": month,
                "celebrating_names": names_list,
                "saints": saints_list,
                "other_info": list(dict.fromkeys(other_info)),
                "names_with_other_dates": has_other_dates_flags,
            }
        )

    if not month_data and len(rows) > 0:
        logger.warning(
            f"No data extracted for month {month}, although rows were present. Check parser logic or source HTML."
        )

    return month_data


@cached(name_search_cache)
def fetch_name_celebration_dates(name: str) -> List[Dict[str, Any]]:
    """
    Fetches and parses celebration dates for a specific name.

    Args:
        name: The name to search for

    Returns:
        List of celebration dates for the name

    Raises:
        HTTPException: If name not found or parsing fails
    """
    logger.info(f"Fetching celebration dates for name: {name}")
    # URL encode the name properly for the path parameter
    encoded_name = urllib.parse.quote(name)
    url = f"{BASE_URL}/pote_giortazei/{encoded_name}"

    response = make_request(url)
    soup = BeautifulSoup(response.text, "lxml")

    # Find the main content area
    content_div = soup.find("div", class_="post-content")
    if not content_div:
        logger.error(f"Could not find 'post-content' div on {url}")
        raise HTTPException(
            status_code=500,
            detail="Could not parse name search results page structure.",
        )

    # Check if the name was found
    h1_tag = content_div.find("h1")
    if not h1_tag or name.lower() not in h1_tag.text.lower():
        if "δεν βρέθηκε" in content_div.text:
            logger.info(
                f"Name '{name}' not found on eortologio.net via /pote_giortazei/"
            )
            raise HTTPException(status_code=404, detail=f"Name '{name}' not found.")
        else:
            logger.warning(
                f"H1 tag mismatch for name '{name}' on {url}, attempting to parse table anyway."
            )

    results_table = content_div.find("table", class_="calendar")
    if not results_table:
        # It's possible a name exists but has no dates listed in the table format
        # Check for alternative text indications if needed
        logger.warning(
            f"No results table (class='calendar') found for name '{name}' on {url}. Name might exist but have no listed dates in table format."
        )
        # Check if the H1 indicated the name exists, if so return empty list
        if h1_tag and name.lower() in h1_tag.text.lower():
            return []
        else:  # If H1 also didn't match, assume not found
            raise HTTPException(
                status_code=404,
                detail=f"Name '{name}' not found or no data available in expected format.",
            )

    celebration_dates = []
    rows = results_table.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 2:  # Need at least date and saint info
            continue

        # --- Extract Date ---
        date_cell = cells[0]
        date_text = date_cell.get_text(
            strip=True
        )  # e.g., "1 Ιουλίου" or "1 Ιουλίου2025 Τρίτη"
        day = None
        month = None
        year = None
        weekday = None

        try:
            # Extract all components: day, month, year, and weekday
            # Pattern for strings like "1 Ιουλίου2025 Τρίτη"
            # Update regex to better capture day of week that might be attached to the year
            date_match = re.match(
                r"(\d+)\s+([Α-Ωα-ωίϊΐόάέύϋΰήώ]+)(?:(\d{4}))?(?:\s*([Α-Ωα-ωίϊΐόάέύϋΰήώ]+))?",
                date_text,
            )

            if date_match:
                day = int(date_match.group(1))
                month_str_genitive = date_match.group(2)
                month = MONTH_NAMES_GREEK_GENITIVE.get(month_str_genitive)
                year = (
                    date_match.group(3)
                    if date_match.group(3)
                    else datetime.now().year + 1
                )  # Default to next year if not specified

                weekday = date_match.group(4)
                if weekday:
                    greek_weekdays = [
                        "Δευτέρα",
                        "Τρίτη",
                        "Τετάρτη",
                        "Πέμπτη",
                        "Παρασκευή",
                        "Σάββατο",
                        "Κυριακή",
                    ]

                    best_match = None
                    for greek_day in greek_weekdays:
                        if weekday in greek_day:
                            if (
                                greek_day.startswith(weekday)
                                or len(weekday) >= len(greek_day) * 0.7
                            ):
                                best_match = greek_day
                                break

                    weekday = best_match if best_match else weekday
                else:
                    weekday = ""

                logger.debug(
                    f"Extracted date components: day={day}, month={month_str_genitive}, year={year}, weekday={weekday}"
                )
            else:
                # Fallback to original splitting logic
                parts = date_text.split()
                if len(parts) >= 2:
                    day = int(parts[0])
                    month_str_genitive = parts[1]
                    month = MONTH_NAMES_GREEK_GENITIVE.get(month_str_genitive)
                    year = datetime.now().year + 1
        except (ValueError, IndexError):
            logger.warning(
                f"Could not parse date string '{date_text}' for name '{name}'"
            )
            continue

        if day is None or month is None:
            logger.warning(
                f"Invalid day or month parsed from '{date_text}' for name '{name}'"
            )
            continue

        # --- Extract Saint Info ---
        saint_cell = cells[1]
        saint_info = saint_cell.get_text(strip=True)
        saint_link = saint_cell.find("a")
        saint_url = (
            saint_link["href"] if saint_link and saint_link.has_attr("href") else None
        )

        # --- Extract Related Names (if available in the 3rd cell) ---
        related_names = []
        if len(cells) > 2:
            names_cell = cells[2]
            # Check if it contains the ">>" marker, indicating it's just a link not names
            if ">>" not in names_cell.text:
                name_links = names_cell.find_all("a")
                for link in name_links:
                    related_name = link.text.strip()
                    if related_name:
                        related_names.append(related_name)
                related_names = list(dict.fromkeys(related_names))  # Deduplicate

        # Format date string in Greek format
        if weekday:
            formatted_date = f"{weekday}, {day} {month_str_genitive} {year}"
        else:
            formatted_date = f"{day} {month_str_genitive} {year}"

        celebration_dates.append(
            {
                "day": day,
                "month": month,
                "date_str": formatted_date,
                "saint_description": saint_info,
                "saint_url": f"{BASE_URL}{saint_url}" if saint_url else None,
                "related_names": related_names,
            }
        )

    # --- Extract Etymology / Other Info ---
    etymology = None

    # Iterate through tags after the table to find etymology
    for tag in results_table.find_next_siblings(["p", "br", "div", "h2", "h3"]):
        if tag.name == "br":
            continue  # Skip breaks

        text_content = tag.get_text(" ", strip=True)
        if not text_content:
            continue

        if "Πιθανή Ετυμολογία" in text_content or "σημαίνει:" in text_content:
            etymology_parts = text_content.split(":", 1)
            if len(etymology_parts) > 1:
                etymology = etymology_parts[1].strip()
            else:  # Handle cases where colon might be missing
                etymology = text_content.replace(
                    "Πιθανή Ετυμολογία / Τι σημαίνει", ""
                ).strip()  # Basic cleanup
            break

    # Add etymology to response if found
    if etymology and celebration_dates:
        # Add to first celebration date entry only
        celebration_dates[0]["etymology"] = etymology

    return celebration_dates
