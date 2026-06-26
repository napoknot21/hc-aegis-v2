from __future__ import annotations

import streamlit as st

from pathlib import Path
from typing import Optional

from src.db.sqlite.crud.quotes import get_random_quote
from src.ui.components.text import margin_line
from src.ui.styles.login import quote_style, author_style


def login_page() -> None:
    """

    """
    _, center, _ = st.columns([1, 3, 1])

    with center:

        login_header()
        login_button()

    quote_section(category="Economics")

    return None


def login_header(logo: Optional[str | Path] = None) -> None:
    """

    """
    margin_line(2)

    _, center, _ = st.columns([1, 8, 1])

    with center:

        logo = (Path(__file__).parent.parent.parent/ "assets" / "logos" / "heroics_aegis_logo.png" if logo is None else Path(logo))
        st.image(str(logo), use_container_width=True)

    margin_line()

    return None


def login_button () -> None :
    """

    """
    margin_line(2)

    _, center, _ = st.columns([1, 1, 1])

    with center :

        if st.button("Login with Microsoft", use_container_width=True) :
            st.login("microsoft")

    margin_line()

    return None


def quote_section(

        category: Optional[str] = "Economics",

        author: Optional[str] = None,
        quote: Optional[str] = None,

    ) -> None:
    """

    """
    info = get_random_quote(category=category)

    if info is None and category is not None :
        info = get_random_quote(category=None)

    if info is None and quote is None :
        return None

    quote = info.get("quote") if quote is None and info is not None else quote
    author = info.get("author") if author is None and info is not None else author

    if quote is None :
        return None

    author = "Unknown" if author is None else author

    margin_line(5)

    st.markdown(f"{quote_style(quote)}{author_style(author)}", unsafe_allow_html=True)

    return None
