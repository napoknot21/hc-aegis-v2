from __future__ import annotations

import datetime as dt
import streamlit as st

from typing import Optional, List, Dict, Any, Tuple

from src.config.parameters import AEGIS_DISC_FUND_HV
from src.utils.formatter import str_to_date
from src.ui.styles.controls import subsections_controls_style


def pnl (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None

    ) :
    """
    
    """
    historical_performance_section(date, fund)
    pnl_breaches = risk_sections(date, fund, )
    
    return pnl_breaches


def historical_performance_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

    ) -> None :
    """
    
    """
    st.title("Hello Workd")


def risk_sections (
        
        date : Optional[str | dt.datetime | dt.datetime] = None,
        fund : Optional[str] = None,

        section : str = "P&L Move",
        icon : str = "📊",

        title : str = "Fund Level",
        risk : str = "PL01",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None

    ) -> Optional[List[Tuple]] :
    """

    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    col1, col2 = st.columns(2)

    with col1 :
        pl01_breaches = PL01_fund_level_section(date, fund, section, icon, user=user, risks=risks) or []

    with col2 :
        pl02_breaches = PL02_book_level_section(date, fund, section, icon, user=user, risks=risks) or []

    return pl01_breaches + pl02_breaches


def PL01_fund_level_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "P&L Move",
        icon : str = "📊",

        title : str = "Fund Level",
        risk : str = "PL01",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None
    
    ) -> Optional[List[Tuple]] :
    """

    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    
    
    return None


def PL02_book_level_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "P&L Move",
        icon : str = "📊",

        title : str = "Book Level",
        risk : str = "PL02",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None
    
    ) -> Optional[List[Tuple]] :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    return None

