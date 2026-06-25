from __future__ import annotations

import streamlit as st

from src.ui.components.text import margin_line


def logout () :
    """
    
    """
    logout_section()

    return None



def logout_section () :
    """
    
    """
    margin_line(2)

    _, center, _ = st.columns([1, 1, 1])
    with center :

        if st.button("Logout") :
            st.logout()

    margin_line()

    return None