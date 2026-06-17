from __future__ import annotations

import os
import numpy as np
import polars as pl
import pandas as pd
import datetime as dt

import streamlit as st

from typing import Optional, Dict, Any, Tuple, List

from src.core.leverages import get_historical_leverage, get_leverage_changes_from_date
from src.utils.formatter import str_to_date
from src.config.parameters import AEGIS_DISC_FUND_HV

from src.ui.components.chart import leverage_line_chart
from src.ui.styles.controls import subsections_controls_style


def controls (
        
        title : str = "📊 CSSF Controls – Metrics and Data",

        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = None,

        user : Optional[str] = None, # This should content information about the user to get or not, different rights / views, etc
    
    ) -> None:
    """
    
    """
    st.write('')
    st.title(title)

    sections = [

        # (Icon, Section, associated function)
        ("📐",  "Leverages",            leverages_section),
        ("📈",  "VaR & SIMM",           var_simm_section),
        ("📊",  "Sensitivities",        sensitivities_section),
        ("📉",  "P&L",                  pnl_section),
        ("💼",  "Counterparty",         counterparty_section),
        ("💳",  "Credit",               credit_section),
        ("⚙️",  "Operational",          operational_section),
        ("🌱",  "ESG",                  esg_section),
        ("✔️",  "Breach Validation",    breach_validation_section)

    ]

    titles = [f"{icon} {t}" for icon, t, _ in sections]
    tab_objs = st.tabs(titles)

    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    breaches = []
    for (icon, section, render_fn), tab in zip(sections, tab_objs) :
        
        with tab :

            breach = render_fn(date, fund, section, icon) or []
            breaches += breach

    st.write(breaches)
    return None


# --------------- Leverage Section ---------------

def leverages_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Leverages",
        icon : str = "📐",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None

    ) -> None :
    """
    
    """
    l01_breaches  = L01_fund_level_section(date, fund, section, icon) or []
    l02_breaches = L02_underlying_level_section(date, fund, section, icon) or []
    l03_breaches = L03_position_level_section(date, fund, section, icon) or []

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
    ) :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    
    dataframe, md5 = get_historical_leverage(date, fund)
    breaches = []

    col1, col2 = st.columns([2, 3])

    with col1 :
        
        title = f"Leverage over time until {date}"
        fig = leverage_line_chart(dataframe, md5, title, date, ["Gross Leverage", "Commitment Leverage"], "Date")

        st.plotly_chart(fig)


    with col2 :
        
        df = get_leverage_changes_from_date(dataframe, md5, date, fund)
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
        
    ) :
    """
    
    """
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
    ) :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    

    return None


# --------------- VaR & SIMM Section ---------------

def var_simm_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,
    ) :
    """
    
    """
    S01_simm_section(date, fund, section, icon)
    S02_im_section(date, fund, section, icon)
    S03_vm_section(date, fund, section, icon)

    return None


def S01_simm_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

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


# --------------- Sensitivies section --------------

def sensitivities_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) -> None :
    """
    
    """
    D01_delta_section(date, fund, section, icon)
    GEQ_gamma_equity_section(date, fund, section, icon)
    GFX_gamma_fx_section(date, fund, section, icon)
    DS01_delta_stress_over_nav_section(date, fund, section, icon)
    DGFX_delta_gamma_fx_adjust(date, fund, section, icon)
    V01_vega_section(date, fund, section, icon)

    return None


def D01_delta_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        title : str = "Delta",
        risk : str = "D01",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,
    
    ) -> None :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    return None


def GEQ_gamma_equity_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        title : str = "Gamma Equity",
        risk : str = "GEQ",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,
    
    ) -> None :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    return None


def GFX_gamma_fx_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        title : str = "Gamma FX",
        risk : str = "GFX",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,

    ) -> None :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    return None


def DS01_delta_stress_over_nav_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        title : str = "Delta Stress over NAV",
        risk : str = "DS01",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,
    
    ) -> None :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    return None


def DGFX_delta_gamma_fx_adjust (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        title : str = "Delta Gamma FX Adjust",
        risk : str = "DGFX",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) -> None :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    return None


def V01_vega_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        title : str = "Vega",
        risk : str = "V01",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) -> None :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    return None


# ------------------- P&L Section -------------------

def pnl_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) -> Optional[List[Tuple]] :
    """
    
    """
    historical_performance_section(date, fund)
    col1, col2 = st.columns(2)

    with col1 :
        PL01_fund_level_section(date, fund, section, icon)

    with col2 :
        PL02_book_level_section(date, fund, section, icon)



    return None


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
    
    ) -> Optional[List[Tuple]] :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    return None


# --------------- Counterparty Section ---------------

def counterparty_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Counterparty",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) -> Optional[List[Tuple]] :
    """
    
    """



def LR01_concentration_risk_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        title : str = "Concentration Risk",
        risk : str = "LR01",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,

    ) -> Optional[List[Tuple]] :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    return None


# --------------- Credit Section ---------------

def credit_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,
    
    ) -> Optional[List[Tuple]] :
    """
    
    """
    cr01_breaches = CR01_concentration_risk_section(date, fund, section, icon, style=style) or []

    return cr01_breaches


def CR01_concentration_risk_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        title : str = "Concentration Risk",
        risk : str = "LR01",

        path_by_fund : Optional[Dict[str]] = None,


        style : str = subsections_controls_style,

    ) -> Optional[List[Tuple]] :
    """
    
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)
    return None




# --------------- Operational Section ---------------

def operational_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) :
    """
    
    """
    st.warning("Data missing")
    return None


# --------------- ESG Section ---------------

def esg_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) :
    """
    
    """
    st.warning("Data missing")
    return None


# --------------- Breach Validation Section -------------

def breach_validation_section (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        section : str = "Credit Risk",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,

        style : str = subsections_controls_style,

    ) :
    """
    
    """
    
    return None




def risks_graphs_and_stats_section () :
    """
    
    """
    return None