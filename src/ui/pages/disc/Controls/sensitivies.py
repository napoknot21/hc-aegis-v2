from __future__ import annotations

import streamlit as st
import datetime as dt

from typing import Optional, Dict, List, Any

from src.ui.styles.controls import subsections_controls_style


def sensitivities (
        
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
