from __future__ import annotations

import streamlit as st

from pathlib import Path
from typing import Optional

from src.config.startup import validate_startup_config, setup

from src.ui.components.layout import sidebar
from src.ui.styles.base import risk_menu

from src.ui.pages.disc.render import render_disc
from src.ui.pages.adv.render import render_adv
from src.ui.pages.admin.render import render_admin
from src.ui.pages.comp.render import render_comp


PAGES = [

    ("Discretionary Management",    "exclamation-triangle-fill",    render_disc),
    ("Advisory",                    "arrow-repeat",                 render_adv),
    ("Compliance",                  "server",                       render_comp),
    ("Administration",              "cash",                         render_admin),

]


def app (
        
        title : Optional[str] = "Heroics Aegis",
        sidebar_state : str = "collapsed"
    
    ) -> None:
    """
    
    """

    if not st.user.is_logged_in :

        st.title("Heroics Aegis")

        if st.button("Login with Microsoft"):
            st.login("microsoft")
    
    else :

        st.set_page_config(title, layout="wide", initial_sidebar_state=sidebar_state)

        name = (st.user.name.split())[0] if st.user.name else "User"
        st.write(f"### Welcome back, {name} !")

        logo = Path(__file__).parent / "assets" / "logos" / "heroics_aegis_logo.png"
        st.image(str(logo), width=300)
        
        
        selected = sidebar(PAGES, f"{name}", logo_header_path=str(logo), styles=risk_menu)
        
        for name, _icon, render in PAGES :

            if selected == name :

                render()
                break

    return None