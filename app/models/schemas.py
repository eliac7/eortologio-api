"""Pydantic models for API request and response schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class NamedayEntry(BaseModel):
    """Schema for a nameday entry."""

    day: int
    month: int
    celebrating_names: List[str]
    saints: List[str]
    other_info: List[str]
    names_with_other_dates: List[str] = Field(default_factory=list)


class CelebrationDate(BaseModel):
    """Schema for a name celebration date entry."""

    day: int
    month: int
    date_str: str
    saint_description: str
    saint_url: Optional[str] = None
    related_names: List[str] = Field(default_factory=list)


class APIResponse(BaseModel):
    """General API response wrapper."""

    message: str
