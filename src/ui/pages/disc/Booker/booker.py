from __future__ import annotations

import streamlit as st
import datetime as dt

from typing import Optional, Dict, List

from src.ui.components.text import margin_line


def booker (
        
        title : str = "📄 Hedge Fund Trade Booking Form",

        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",
    
    ) -> None:
    """
    
    """
    margin_line()
    st.title(title)
    
    

    return None
