from __future__ import annotations

import os
import numpy as np
import polars as pl
import pandas as pd
import datetime as dt

import streamlit as st

from typing import Optional, Dict, Any, Tuple, List

from src.config.parameters import AEGIS_DISC_FUND_HV, AEGIS_RISKS
from src.utils.formatter import str_to_date
from src.core.risk import build_risk_background_ranges

from src.ui.components.text import margin_line
from src.ui.styles.controls import subsections_controls_style

from src.ui.pages.disc.Controls.leverages import leverages
from src.ui.pages.disc.Controls.var_simm import var_simm
from src.ui.pages.disc.Controls.sensitivies import sensitivities
from src.ui.pages.disc.Controls.pnl import pnl
from src.ui.pages.disc.Controls.counterparty import counterparty
from src.ui.pages.disc.Controls.credit import credit
from src.ui.pages.disc.Controls.operational import operational
from src.ui.pages.disc.Controls.breaches import breaches_validator


def controls (
        
        title : str = "📊 CSSF Controls – Metrics and Data",

        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = None,

        user : Optional[Any] = None, # This should content information about the user to get or not, different rights / views, etc
        risks : Optional[Dict] = None
    
    ) -> None:
    """
    
    """
    margin_line()
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

    risks = AEGIS_RISKS if risks is None else risks

    breaches = []
    for (icon, section, render_fn), tab in zip(sections, tab_objs) :
        
        with tab :

            breach = render_fn(date, fund, section, icon, user=user, risks=risks, breaches=breaches) or []
            breaches += breach


    return None


# --------------- Leverage Section ---------------

def leverages_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Leverages",
        icon : str = "📐",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,


    ) -> None :
    """
    
    """
    leverages_breaches = leverages(date, fund, section, icon, user, risks)

    return leverages_breaches


# --------------- VaR & SIMM Section ---------------

def var_simm_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,

    ) :
    """
    
    """
    var_simm_breaches = var_simm(date, fund, section, icon, path_by_fund)

    return var_simm_breaches


# --------------- Sensitivies section --------------

def sensitivities_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,

    ) -> None :
    """
    
    """
    sensitivies_breaches = sensitivities(date, fund, section, icon, user, risks)

    return sensitivies_breaches


# ------------------- P&L Section -------------------

def pnl_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Sensitivities",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,

    ) -> Optional[List[Tuple]] :
    """
    
    """
    pnl_breaches = pnl(date, fund, section, icon, user, risks)

    return pnl_breaches


# --------------- Counterparty Section ---------------

def counterparty_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Counterparty",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,

    ) -> Optional[List[Tuple]] :
    """
    
    """
    ctpy_breaches = counterparty(date, fund, section, icon, path_by_fund)

    return ctpy_breaches


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
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,
    
    ) -> Optional[List[Tuple]] :
    """
    
    """
    cr01_breaches = credit(date, fund, section, icon, style=style) or []

    return cr01_breaches


# --------------- Operational Section ---------------

def operational_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,

    ) :
    """
    
    """
    operational_breaches = operational(date, fund, section, icon)

    return operational_breaches


# --------------- ESG Section ---------------

def esg_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "Credit Risk",
        icon : str = "📊",

        path_by_fund : Optional[Dict[str]] = None,    
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
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
        sub_menus : Optional[Dict[str]] = None,

        user : Optional[Any] = None, # Check the User rights
        risks : Optional[Dict] = None,

        breaches : Optional[List[Tuple]] = None,
        style : str = subsections_controls_style,

    ) :
    """
    
    """
    breaches_validator(date, fund, breaches=breaches)
    return None


# ---------------  Section -------------

def risks_graphs_and_stats_section () :
    """
    
    """
    return None
