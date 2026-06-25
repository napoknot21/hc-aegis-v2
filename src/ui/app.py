from __future__ import annotations

import asyncio
import sys

import streamlit as st

from pathlib import Path
from typing import Optional

from src.config.startup import validate_startup_config, setup

from src.ui.components.layout import sidebar
from src.ui.styles.base import risk_menu

from src.ui.pages.login.login import login_page

from src.ui.pages.disc.render import render_disc
from src.ui.pages.adv.render import render_adv
from src.ui.pages.admin.render import render_admin
from src.ui.pages.comp.render import render_comp

from src.db.sqlite.connection import init_database


PAGES = [

    ("Discretionary Management",    "exclamation-triangle-fill",    render_disc),
    ("Advisory",                    "arrow-repeat",                 render_adv),
    ("Compliance",                  "server",                       render_comp),
    ("Administration",              "cash",                         render_admin),
    #("R&D",                        "server",                       render_r_n_d),
]



def app (
        
        title : Optional[str] = "Heroics Aegis",
        sidebar_state : str = "collapsed"
    
    ) -> None:
    """
    
    """
    init_database(seed=True)

    #if not st.user.is_logged_in :

    #    login_page()
    #    return None
    

    st.set_page_config(title, layout="wide", initial_sidebar_state=sidebar_state)

    logo = Path(__file__).parent / "assets" / "logos" / "heroics_aegis_logo.png"
    st.image(str(logo), width=300)

    user_name = getattr(st.user, "name", None)
    name = user_name.split()[0] if user_name else "User"
    
    st.write(f"### Welcome back, {name} !")
    
    selected, selected_date, selected_fund = sidebar("Heroics Capital", PAGES, logo_header_path=str(logo), styles=risk_menu)
    
    for name, _icon, render in PAGES :

        if selected == name :

            render(date=selected_date, fund=selected_fund)
            break

    return None
