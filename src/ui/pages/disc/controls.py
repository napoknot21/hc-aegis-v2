from __future__ import annotations

import os
import numpy as np
import polars as pl
import pandas as pd
import datetime as dt

import streamlit as st

from typing import Optional, Dict

from src.config.parameters import AEGIS_DISC_CONTROLS_SUB_MENUS
from src.utils.formater import str_to_date


def controls (date, fund) :
    """
    
    """
    tabs = controls_menu(date, fund)
    
    st.write(len(tabs))
    return None





def controls_menu (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None
        
    ) -> None :
    """
    
    """
    date = str_to_date(date)
    fund = "HV" if fund is None else fund

    path_by_fund = None if path_by_fund is None else path_by_fund
    fund_path = path_by_fund.get(fund) if path_by_fund is not None else None

    sub_menus = AEGIS_DISC_CONTROLS_SUB_MENUS if sub_menus is None else sub_menus

    tabs_with_icons = [f"{sub_menu['icon']} {sub_menu['menu']}" for sub_menu in sub_menus]
    tabs = st.tabs(tabs_with_icons)

    print(tabs)

    return None
    