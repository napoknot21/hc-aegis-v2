from __future__ import annotations

import streamlit as st
import datetime as dt

from streamlit_option_menu import option_menu

from typing import Optional, Dict

from src.ui.pages.disc.controls import controls
from src.ui.pages.disc.updater import updater


discretionary_subpages = [

    {"name" : "Booker IA",           "page" : controls,  "icon" : "currency-exchange"},
    {"name" : "Deleter",             "page" : controls,  "icon" : "archive-fill"},
    {"name" : "Updater",             "page" : updater,   "icon" : "node-plus-fill"},
    {"name" : "Viewer",              "page" : controls,  "icon" : "file-spreadsheet-fill"},
    {"name" : "Regulatory Controls", "page" : controls,  "icon" : "file-spreadsheet-fill"},

]



def render_disc (

        title : Optional[str] = "",
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