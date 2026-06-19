from __future__ import annotations

import datetime as dt
import streamlit as st

from typing import Optional, Dict, Any, List

from src.config.parameters import AEGIS_DISC_FUND_HV, AEGIS_RISKS
from src.core.risk import build_risk_background_ranges
from src.utils.formatter import str_to_date

from src.core.leverages import get_historical_leverage, get_leverage_changes_from_date

from src.ui.styles.controls import subsections_controls_style
from src.ui.components.chart import leverage_line_chart
from src.ui.components.text import margin_line

# --------------- Leverage Section ---------------

def leverages (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Leverages",
        icon : str = "📐",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None,

    ) -> Optional[List[Any]] :
    """
    
    """
    l01_breaches  = L01_fund_level_section(date, fund, section, icon, user=user, risks=risks) or []
    l02_breaches = L02_underlying_level_section(date, fund, section, icon, user=user, risks=risks) or []
    l03_breaches = L03_position_level_section(date, fund, section, icon, user=user, risks=risks) or []

    return l01_breaches + l02_breaches + l03_breaches


def L01_fund_level_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Leverage Risk",
        icon : str = "📐",
        title : str = "Fund Level",
        risk : str = "L01",

        path_by_fund : Optional[Dict[str]] = None,
        limits : Optional[Any] = None,

        style : str = subsections_controls_style,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None,

    ) :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    risks = AEGIS_RISKS if risks is None else risks
    risk_config = risks.get(risk, None)

    if risk_config is None :

        st.write(f"No Risk config for {risk}")
        return None

    limits = build_risk_background_ranges(risk_config) if limits is None else limits

    dataframe, md5 = get_historical_leverage(date, fund)
    breaches = []

    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 3])

    with col1 :
        
        title = f"Leverage over time until {date}"
        fig = leverage_line_chart(dataframe, md5, title, date, ["Gross Leverage", "Commitment Leverage"],"Date",
            background_ranges=limits,
        )

        st.plotly_chart(fig)


    with col2 :
        
        df = get_leverage_changes_from_date(dataframe, md5, date, fund)

        margin_line(2)
        st.dataframe(df)

    return breaches


def L02_underlying_level_section (
               
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Leverage Risk",
        icon : str = "📐",
        title : str = "Underlying Level",
        risk : str = "L02",

        path_by_fund : Optional[Dict[str]] = None,
        limits : Optional[Any] = None,

        style : str = subsections_controls_style,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None,
        
    ) :
    """
    
    """
    limits = build_risk_background_ranges(_get_risk_config(risk, risks)) if limits is None else limits

    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    breaches = [(risk, f"{section}", dt.datetime.now()), (risk, f"{section}", dt.datetime.now())]

    return breaches


def L03_position_level_section (

        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Leverage Risk",
        icon : str = "📐",
        title : str = "Position Level",
        risk : str = "L03",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,

        user : Optional[Any] = None,
        risks : Optional[Dict] = None,
    ) :
    """
    
    """
    limits = build_risk_background_ranges(_get_risk_config(risk, risks))

    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    

    return None


def _get_risk_config (

        risk : str,
        risks : Optional[Dict[str, Any]] = None,

    ) -> Optional[Dict[str, Any]] :
    """
    Resolve one risk configuration from the global AEGIS_RISKS mapping.
    """
    risks = AEGIS_RISKS if risks is None else risks

    return risks.get(risk)

