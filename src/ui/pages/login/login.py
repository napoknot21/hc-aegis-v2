from __future__ import annotations

import streamlit as st
import datetime as dt

from pathlib import Path
from typing import Optional

from src.db.sqlite.crud.quotes import get_random_quote
from src.ui.components.text import margin_line


def login_page () -> None :
    """
    
    """
    _, center, _ = st.columns([1, 2, 1])

    with center :
        
        login_header()
        login_button()
        quote_section()

    return None



def login_header (logo : Optional[str | Path] = None) -> None :
    """
    
    """
    margin_line(2)
    
    logo = Path(__file__).parent.parent.parent / "assets" / "logos" / "heroics_aegis_logo.png" if logo is None else logo
    st.image(str(logo), width=300)

    margin_line()

    return None



def login_button () -> None :
    """
    
    """
    margin_line(2)

    _, center, _ = st.columns([1, 2, 1])
    
    with center :

        if st.button("Login with Microsoft"):
            st.login("microsoft")

    margin_line()

    return None



def quote_section () -> None:
    """
    
    """
    info = get_random_quote("Economics")
    st.write(info)
    return None
