from __future__ import annotations

import base64
import datetime as dt

from typing import Optional


def date_to_str (date : Optional[str | dt.datetime] = None, format : str = "%Y-%m-%d") -> str :
    """
    Convert a date or datetime object to a string in "YYYY-MM-DD" format.

    Args:
        date (str | datetime): The input date.

    Returns:
        str: Date string in "YYYY-MM-DD" format.
    """
    if date is None:
        date_obj = dt.datetime.now()

    elif isinstance(date, dt.datetime):
        date_obj = date

    elif isinstance(date, dt.date):  # handles plain date (without time)
        date_obj = dt.datetime.combine(date, dt.time.min) # This will add 00 for the time

    elif isinstance(date, str) :

        try:
            date_obj = dt.datetime.strptime(date, format)

        except ValueError :
            
            try :
                date_obj = dt.datetime.fromisoformat(date)
            
            except ValueError :
                raise ValueError(f"Unrecognized date format: '{date}'")
    
    else :
        raise TypeError("date must be a string, datetime, or None")

    return date_obj.strftime(format)


def str_to_date (date : Optional[str | dt.date | dt.datetime] = None, format : str = "%Y-%m-%d") -> dt.date :
    """
    Convert a string, date, datetime, or None value to `datetime.date`.

    Strings are parsed using the provided format. `None` returns today's date.
    """
    if date is None :
        date_obj = dt.date.today()
    
    if isinstance (date, dt.datetime):
        date_obj = date.date()

    if isinstance(date, dt.date) :
        date_obj = date
    
    if isinstance(date, str) :
        date_obj = dt.datetime.strptime(date, format).date()
    
    return date_obj


def convert_bytes_64 (file_abs_path : Optional[str]) -> Optional[str] :
    """
    Read a file and return its base64-encoded content.

    Returns `None` when no path is supplied.
    """

    if file_abs_path is None :
        return None

    with open(file_abs_path, "rb") as f :
        base64_cont = base64.b64encode(f.read()).decode('utf-8')

    return base64_cont
