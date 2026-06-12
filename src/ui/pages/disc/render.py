from __future__ import annotations

import streamlit as st
import datetime as dt

from streamlit_option_menu import option_menu

from typing import Optional, Dict

from src.ui.pages.disc.controls import controls
from src.ui.pages.disc.updater import updater


discretionary_subpages = [

    {"name" : "Controls",       "page" : controls,  "icon" : "cash-coin"},
    {"name" : "Updater",        "page" : updater,   "icon" : "eye"},

]



def render_disc (

        title : Optional[str] = "Discretionary Management",
        subtitle : Optional[str] = None,
        fundation_map : Optional[Dict] = None

    ) :
    """
    
    """
    st.title(title)

    selected_page = option_menu(
        None, 
        [p['name'] for p in discretionary_subpages], 
        icons=[p['icon'] for p in discretionary_subpages], 
        default_index=0,
        orientation="horizontal"
    )

    return None