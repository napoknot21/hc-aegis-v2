from __future__ import annotations

import datetime as dt
from typing import Optional, List

from src.utils.formatter import date_to_str, str_to_date


def get_previous_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d"

    ) -> Optional[dt.date] :
    """
    Get the previous business day from a given date.
    
    Args:
        date (str): The input date in "YYYY-MM-DD" format.
    
    Returns:
        str: The previous business day in "YYYY-MM-DD" format.
    """
    date = str_to_date(date, format)
    return None


def get_ytd_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d",

    ) -> Optional[dt.date] :
    """
    
    """
    date = str_to_date(date, format)
    # Something here
    return None


def get_qtd_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d",

    ) -> Optional[dt.date] :
    """
    
    """
    date = str_to_date(date)
    return None



def get_1m_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d",

    ) -> Optional[dt.date] :
    """
    
    """
    date = str_to_date(date)
    return None


def get_1w_bussiness_day (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        format : str = "%Y-%m-%d",

    ) -> Optional[dt.date] :
    """
    
    """
    date = str_to_date(date)
    return None


