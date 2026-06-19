from __future__ import annotations

import streamlit as st
import datetime as dt

from typing import Optional, Dict, List, Any, Tuple

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

    col1, col2 = st.columns(2)

    with col1 :
        pl01_breaches = PL01_fund_level_section(date, fund, section, icon, user=user, risks=risks) or []

    with col2 :
        pl02_breaches = PL02_book_level_section(date, fund, section, iconuser=user, risks=risks) or []

    return pl01_breaches + pl02_breaches



def historical_performance_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

    ) -> None :
    """
    
    """
    st.title("Hello Workd")


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

