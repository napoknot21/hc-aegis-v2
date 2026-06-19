from __future__ import annotations

import streamlit as st
import datetime as dt

from streamlit_option_menu import option_menu

from typing import Optional, Dict

from src.ui.components.text import margin_line

from src.ui.pages.disc.Booker.booker import booker
from src.ui.pages.disc.Controls.controls import controls
from src.ui.pages.disc.Updater.updater import updater

discretionary_subpages = [

    {"name" : "Booker IA",           "page" : booker,    "icon" : "currency-exchange"},
    {"name" : "Deleter",             "page" : controls,  "icon" : "archive-fill"},
    {"name" : "Updater",             "page" : updater,   "icon" : "node-plus-fill"},
    {"name" : "Viewer",              "page" : controls,  "icon" : "file-spreadsheet-fill"},
    {"name" : "Regulatory Controls", "page" : controls,  "icon" : "file-spreadsheet-fill"},

]



def render_disc (

        title : Optional[str] = "",
        subtitle : Optional[str] = None,
        fundation_map : Optional[Dict] = None,
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = None

    ) :
    """
    
    """
    margin_line(2)

    menu = option_menu(
        
        None, 
        [subpage['name'] for subpage in discretionary_subpages], 
        icons=[subpage['icon'] for subpage in discretionary_subpages], 
        orientation="horizontal",
        default_index=0,
    
    )

    for subpage in discretionary_subpages :
        
        if menu == subpage['name'] and not subpage['page'] is None :
            subpage['page'](date=date, fund=fund)

    return None
