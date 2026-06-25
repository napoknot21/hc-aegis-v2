from __future__ import annotations

import datetime as dt

import streamlit as st
from streamlit_option_menu import option_menu

from pathlib import Path
from typing import List, Dict, Optional, Tuple

from src.config.parameters import AEGIS_DISC_FUNDS
from src.ui.components.text import center_h2
from src.ui.components.selector import date_selector
from src.ui.pages.login.logout import logout

def header (
        
        title : Optional[str] = None,
        subtitle : Optional[str] = None,
        logo_path : Optional[str | Path] = None,
        logo_width : int = 300,
        center : bool = True
    
    ) :
    """
    
    """
    p = Path(logo_path)

    if center :

        col_left, col_center, col_right = st.columns([1, 2, 1])
        
        with col_center:
        
            if p.exists():
                st.image(str(p), width=logo_width)
        
            if title:
                st.markdown(
                    f"<h1 style='text-align:center;margin:0'>{title}</h1>",
                    unsafe_allow_html=True,
                )

            if subtitle:
                st.markdown(
                    f"<div style='text-align:center;opacity:.75'>{subtitle}</div>",
                    unsafe_allow_html=True,
                )
    else :

        if p.exists() :
            st.image(str(p))#, width="stretch")
        
        if title :
            st.markdown(f"## {title}")
        
        if subtitle :
            st.caption(subtitle)

    return None


def sidebar (
        
        title : str = "",
        groupes : Optional[List[Dict[str, str]]] = None,
        funds : Optional[Dict] = None,

        logo_header_path : Optional[str] = None,
        styles : Optional[Dict] = None
    
    ) -> Tuple[str, dt.date, str] :
    """
    From a group of tabs, it will create a graphical sidebar
    """
    names = [p[0] for p in groupes]
    icons = [p[1] for p in groupes]

    funds = AEGIS_DISC_FUNDS if funds is None else funds
    sidebar = st.sidebar

    with sidebar:

        if logo_header_path:
            st.image(logo_header_path)#, width='stretch')

        center_h2(title)
        
        selected = option_menu(None, names, icons=icons, styles=styles)
        st.cache_data.clear()

        st.divider()

        selected_date = date_selector("Date", key="aegis_global_date")
        selected_fund = st.selectbox("Fund", list(funds.keys()), key="aegis_sidebar_fund")

        st.divider()

        footer_aegis("https://sentinelle.heroics-capital.com")

        #if st.user.is_logged_in :
        logout()

    # update query params for deep linking
    st.query_params["page"] = selected
    
    return selected, selected_date, selected_fund





def footer_aegis (link : Optional[str] = None) :
    """
    
    """
    if link :

        aegis = st.link_button("Heroics Sentinelle", link)

    return aegis

    
