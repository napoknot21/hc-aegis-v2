from __future__ import annotations

import datetime as dt
from typing import Optional, List

from utils.formatter import date_to_str, str_to_date


def get_previous_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d"

    ) -> str :
    """
    Get the previous business day from a given date.
    
    Args:
        date (str): The input date in "YYYY-MM-DD" format.
    
    Returns:
        str: The previous business day in "YYYY-MM-DD" format.
    """
    return None