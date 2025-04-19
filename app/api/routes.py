"""API routes for the nameday service."""

from datetime import date, timedelta
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Path

from app.services.nameday_service import (
    fetch_and_parse_month_data,
    fetch_name_celebration_dates,
)
from app.core.config import logger
from app.models.schemas import NamedayEntry, CelebrationDate, APIResponse

router = APIRouter()


@router.get(
    "/today", response_model=NamedayEntry, summary="Get today's nameday information"
)
async def get_today_nameday() -> Dict[str, Any]:
    """
    Returns the list of names celebrating today and the associated saints/feasts.
    Uses cached monthly data.
    """
    today = date.today()
    current_month = today.month
    current_day = today.day

    try:
        month_data = fetch_and_parse_month_data(current_month)
    except Exception as e:
        logger.error(f"Error getting data for today (month {current_month}): {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail=f"Internal error processing today's data: {str(e)}"
        )

    for day_info in month_data:
        if (
            day_info.get("day") == current_day
            and day_info.get("month") == current_month
        ):
            return day_info

    logger.warning(f"No data found for today ({today}) in month {current_month}.")
    raise HTTPException(
        status_code=404, detail=f"No nameday information found for today ({today})."
    )


@router.get(
    "/tomorrow",
    response_model=NamedayEntry,
    summary="Get tomorrow's nameday information",
)
async def get_tomorrow_nameday() -> Dict[str, Any]:
    """
    Returns the list of names celebrating tomorrow and the associated saints/feasts.
    Uses cached monthly data.
    """
    tomorrow = date.today() + timedelta(days=1)
    target_month = tomorrow.month
    target_day = tomorrow.day

    try:
        month_data = fetch_and_parse_month_data(target_month)
    except Exception as e:
        logger.error(f"Error getting data for tomorrow (month {target_month}): {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Internal error processing tomorrow's data: {str(e)}",
        )

    for day_info in month_data:
        if day_info.get("day") == target_day and day_info.get("month") == target_month:
            return day_info

    logger.warning(f"No data found for tomorrow ({tomorrow}) in month {target_month}.")
    raise HTTPException(
        status_code=404,
        detail=f"No nameday information found for tomorrow ({tomorrow}).",
    )


@router.get(
    "/month",
    response_model=List[NamedayEntry],
    summary="Get nameday information for the current month",
)
async def get_current_month_namedays() -> List[Dict[str, Any]]:
    """
    Returns a list of all nameday entries for the current calendar month.
    Uses cached monthly data.
    """
    current_month = date.today().month
    try:
        return fetch_and_parse_month_data(current_month)
    except Exception as e:
        logger.error(f"Error getting data for current month ({current_month}): {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Internal error processing current month's data: {str(e)}",
        )


@router.get(
    "/month/{month_num}",
    response_model=List[NamedayEntry],
    summary="Get nameday information for a specific month",
)
async def get_specific_month_namedays(
    month_num: int = Path(
        ..., title="Month Number", description="Month number (1-12)", ge=1, le=12
    )
) -> List[Dict[str, Any]]:
    """
    Returns a list of all nameday entries for the specified month number (1-12).
    Uses cached monthly data.
    """
    try:
        return fetch_and_parse_month_data(month_num)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid month number. Must be between 1 and 12."
        )
    except Exception as e:
        logger.error(f"Error getting data for month {month_num}: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Internal error processing data for month {month_num}: {str(e)}",
        )


@router.get(
    "/search/{name}",
    response_model=List[CelebrationDate],
    summary="Search celebration dates for a specific name (direct lookup)",
)
async def search_name_dates_direct(
    name: str = Path(
        ..., title="Name to Search", description="The Greek name to search for"
    )
) -> List[Dict[str, Any]]:
    """
    Searches for celebration dates for the specified name using the direct
    `eortologio.net/pote_giortazei/` endpoint. Results are cached per name.
    """
    clean_name = name.strip()
    if not clean_name:
        raise HTTPException(status_code=400, detail="Name parameter cannot be empty.")

    try:
        return fetch_name_celebration_dates(clean_name)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(
            f"Unexpected error searching for name '{clean_name}': {e}", exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error while searching for name '{clean_name}'.",
        )


@router.get("/", response_model=APIResponse, summary="API Root/Health Check")
async def read_root():
    return {"message": "Greek Nameday API is running. See /docs for details."}
