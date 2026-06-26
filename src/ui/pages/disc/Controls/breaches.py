from __future__ import annotations

import datetime as dt
import streamlit as st

from typing import List, Optional, Dict, Tuple

from src.config.parameters import AEGIS_DISC_FUND_HV
from src.utils.formatter import str_to_date

from src.ui.components.chat import chat
from src.ui.components.text import margin_line

from src.ui.styles.controls import subsections_controls_style
from src.ui.styles.breaches import breaches_title_style



def breaches_validator (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        title : Optional[str] = "🧾 Breach Validation Panel",
        user : Optional[str] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,

    ) :
    """


    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    st.markdown(f"{breaches_title_style(title)}", unsafe_allow_html=True)
    margin_line(2)

    runners_section(date, fund, user, breaches)
    breaches_chat_section(date, fund)

    return None



def runners_section (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        user : Optional[str] = None,
        breaches : Optional[List[Tuple]] = None,

    ) -> None :
    """

    """
    breaches = [] if breaches is None else breaches

    col1, _ = st.columns(2, gap=None)

    with col1 :

        runner, loader = st.columns(2, gap=None)

        with runner :
            breach_analysis_runner(date, fund, breaches)

        with loader :
            data_breach_loader(date, fund)
    
    return None


def breach_analysis_runner (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        breaches : Optional[List[Tuple]] = None,

    ) -> None :
    """
    
    """
    with st.spinner("Running full breach analysis...") :
    
        if st.button("🚨 Breach Analysis Runner", type="primary"):
            st.write("")

    return None


def data_breach_loader (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

    ) -> None :
    """
    
    """
    with st.spinner("Running full breach analysis...") :
    
        if st.button("🚨 Data Breach Loader", type="primary"):
            st.write("")


    return None


def breaches_chat_section (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

    ) -> None :
    """

    """

    col1, col2 = st.columns([2, 3])

    with col1 :
        chat_breaches_section()

    with col2 :
        st.write("Hello")

    return None



def chat_breaches_section (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        user : Optional[str] = None
    
    ) :
    """

    """

    #chat("Unknownw")
    return None



def breaches_data_section (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None

    ) -> None :
    """

    """
    
    return None