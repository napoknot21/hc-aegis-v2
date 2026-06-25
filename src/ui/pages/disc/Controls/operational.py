from __future__ import annotations

import datetime as dt
import streamlit as st

from typing import Optional, List, Dict, Any

from src.config.parameters import AEGIS_DISC_FUND_HV
from src.utils.formatter import str_to_date
from src.ui.styles.controls import subsections_controls_style

def operational (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Operational",
        icon : str = "",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None,
    
    ) :
    """

    """
    st.warning("Data Missing")
    operational_breaches = []

    return operational_breaches