from __future__ import annotations

import streamlit as st
import datetime as dt

from typing import Optional

from src.utils.formatter import str_to_date


def date_selector (
        
        label : Optional[str] = "Select a Date",
        default : Optional[str | dt.datetime | dt.date]= None,
        key : str = "Date"

    ) -> Optional[dt.date] :
    """
    
    """

    default = dt.date.today() if default is None else default
    
    date = st.date_input(label, value=default, key=key)
    date = str_to_date(date)

    return date
