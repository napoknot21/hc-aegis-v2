from __future__ import annotations

import datetime as dt
import streamlit as st

from typing import Optional, List, Dict, Any, Tuple

from src.ui.styles.controls import subsections_controls_style


def credit (
        
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
        
    ) -> None :
    """

    """

    return []



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

