from __future__ import annotations

import threading
import streamlit as st

from typing import Optional

from src.ui.pages.disc.render import render_disc
from src.ui.pages.adv.render import render_adv
from src.ui.pages.admin.render import render_admin
from src.ui.pages.comp.render import render_comp


def app (
        
        title : Optional[str] = "Heroics Aegis",
        sidebar_state : str = "collapsed"
    
    ) -> None:
    """
    
    """
    st.set_page_config(title, layout="wide", initial_sidebar_state=sidebar_state)

    return None