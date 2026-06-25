from __future__ import annotations

import datetime as dt
import streamlit as st

from typing import Optional, Dict, List, Tuple

from src.config.parameters import AEGIS_DISC_FUND_HV
from src.utils.formatter import str_to_date
from src.ui.styles.controls import subsections_controls_style


def counterparty (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        style : Optional[str] = None,
        breaches : Optional[List[Tuple]] = None,

    ) -> Optional[List[Tuple]] :
    """

    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    return None



def CR01_concentration_risk (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None
    
    ) :
    """

    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    return None