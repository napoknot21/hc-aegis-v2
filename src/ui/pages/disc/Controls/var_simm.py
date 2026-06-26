from __future__ import annotations

import polars as pl
import datetime as dt
import streamlit as st

from typing import Optional, Dict, List, Any

from src.config.parameters import AEGIS_DISC_FUND_HV
from src.utils.formatter import str_to_date, date_to_str
from src.ui.styles.controls import subsections_controls_style
from src.ui.components.text import margin_line
from src.core.simm import get_im_ctpy_all_history, get_im_ice_all_history, get_im_ctpy_by_date



def var_simm (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

    ) -> Optional[List[Any]] :
    """
    
    """
    s01_breaches = S01_simm_section(date, fund, section, icon) or []
    s02_breaches = S02_im_section(date, fund, section, icon) or []
    s03_breaches = S03_vm_section(date, fund, section, icon) or []

    return s01_breaches + s02_breaches + s03_breaches


def S01_simm_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = None,

        section : str = "VaR/SIMM",
        icon : str = "📈",

        title : str = "SiMM",
        risk : str = "S01",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,
    ) :
    """
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund)
    st.dataframe(dataframe)
    margin_line()

    df, md = get_im_ice_all_history(date, fund)
    st.dataframe(df)

    date_df, _ , real_date= get_im_ctpy_by_date(date, fund)
    st.dataframe(date_df)
    st.write(real_date)
    return None


def S02_im_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        title : str = "IM",
        risk : str = "S02",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,
    ) :
    """
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    
    return None


def S03_vm_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        title : str = "VM",
        risk : str = "S03",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,
    ) :
    """
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    
    return None

