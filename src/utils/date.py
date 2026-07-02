from __future__ import annotations

import datetime as dt
from typing import Optional

from src.utils.formatter import date_to_str, str_to_date




def get_previous_bussiness_day (
        
        date: Optional[str | dt.datetime | dt.date] = None,
        format: str = "%Y-%m-%d",
    
    ) -> Optional[dt.date]:
    """
    Get the previous business day strictly before the given date.

    Example:
        Monday    -> previous Friday
        Sunday    -> previous Friday
        Wednesday -> previous Tuesday
    """
    date = str_to_date(date, format)

    if date is None:
        return None

    return _previous_weekday(date)


def get_ytd_bussiness_day (
        
        date: Optional[str | dt.datetime | dt.date] = None,
        format: str = "%Y-%m-%d",
    
    ) -> Optional[dt.date]:
    """
    Get the first business day of the year of the given date.
    """
    date = str_to_date(date, format)

    if date is None:
        return None

    start_of_year = dt.date(date.year, 1, 1)

    return _next_weekday(start_of_year)


def get_qtd_bussiness_day (
        
        date: Optional[str | dt.datetime | dt.date] = None,
        format: str = "%Y-%m-%d",
    
    ) -> Optional[dt.date]:
    """
    Get the first business day of the quarter of the given date.
    """
    date = str_to_date(date, format)

    if date is None:
        return None

    quarter_start_month = ((date.month - 1) // 3) * 3 + 1
    start_of_quarter = dt.date(date.year, quarter_start_month, 1)

    return _next_weekday(start_of_quarter)


def get_1m_bussiness_day (
        
        date: Optional[str | dt.datetime | dt.date] = None,
        format: str = "%Y-%m-%d",
    
    ) -> Optional[dt.date]:
    """
    Get the business day one month before the given date.

    If the same day does not exist in the previous month, use the last valid
    calendar day of the previous month, then adjust to previous weekday if needed.

    Example:
        2024-03-31 -> 2024-02-29
        2024-03-30 -> 2024-02-29
        2024-05-31 -> 2024-04-30
    """
    date = str_to_date(date, format)

    if date is None:
        return None

    if date.month == 1:
        target_year = date.year - 1
        target_month = 12
    else:
        target_year = date.year
        target_month = date.month - 1

    # First day of the month after target month
    if target_month == 12:
        next_month = dt.date(target_year + 1, 1, 1)
    else:
        next_month = dt.date(target_year, target_month + 1, 1)

    last_day_of_target_month = next_month - dt.timedelta(days=1)

    target_day = min(date.day, last_day_of_target_month.day)
    target_date = dt.date(target_year, target_month, target_day)

    return _previous_or_same_weekday(target_date)


def get_1w_bussiness_day (
        
        date: Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d",

    ) -> Optional[dt.date] :
    """
    Get the business day one week before the given date.

    Since subtracting 7 calendar days preserves the weekday, this only needs
    weekend adjustment if the input date itself is on a weekend.
    """
    date = str_to_date(date, format)
    target_date = date - dt.timedelta(weeks=1)

    return _previous_or_same_weekday(target_date)


def today_previous_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d",

    ) -> Optional[dt.date] :
    """
    Check if a date is a week day or previous business day otherwise from today.
    """
    date = str_to_date(date, format)

    if date.weekday() != 5 and date.weekday() != 6:
        return date

    while date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        date = date - dt.timedelta(days=1)

    return date


def today_next_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d",

    ) -> Optional[dt.date] :
    """
    Check if a date is a week day or previous business day otherwise from today.
    """
    date = str_to_date(date, format)

    if date.weekday() != 5 and date.weekday() != 6:
        return date

    while date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        date = date + dt.timedelta(days=1)

    return date


def _previous_weekday (date: dt.date) -> dt.date:
    """
    Return the previous weekday strictly before `date`.
    Weekdays are Monday-Friday.
    """
    date = date - dt.timedelta(days=1)

    while date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        date = date - dt.timedelta(days=1)

    return date


def _next_weekday (date: dt.date) -> dt.date:
    """
    Return `date` if it is a weekday, otherwise the next weekday.
    """
    while date.weekday() >= 5:
        date = date + dt.timedelta(days=1)

    return date


def _previous_or_same_weekday (date : dt.date) -> dt.date:
    """
    Return `date` if it is a weekday, otherwise the previous weekday.
    """
    while date.weekday() >= 5:
        date = date - dt.timedelta(days=1)

    return date