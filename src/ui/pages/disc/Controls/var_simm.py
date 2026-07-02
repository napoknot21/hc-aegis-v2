from __future__ import annotations

import datetime as dt
import streamlit as st

from typing import Optional, Dict, List, Any

from src.config.parameters import AEGIS_DISC_FUND_HV, RENAME_COUNTERPARTY_MAP
from src.utils.formatter import str_to_date
from src.ui.styles.controls import subsections_controls_style, simm_colored_card
from src.ui.components.text import margin_line
from src.ui.components.table import render_changes_table
from src.core.data.simm.im import (
    get_im_ctpy_all_history,
    get_im_ctpy_changes_from_date,
    get_im_ice_all_history,
    get_im_ice_changes_from_date,
)
from src.core.data.simm.simm import get_simm_nav_changes_from_date
from src.core.data.simm.vm import (
    get_vm_ctpy_all_history,
    get_vm_ctpy_changes_from_date,
    get_vm_ice_all_history,
    get_vm_ice_changes_from_date,
)

from src.ui.components.graph import plot_im_by_bank, plot_vm_by_bank, render_plotly_chart


def var_simm (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

    ) -> Optional[List[Any]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    nav = 85231771.0
    s01_breaches = S01_simm_section(date, fund, section, icon, nav=nav) or []
    s02_breaches = S02_im_section(date, fund, section, icon, nav=nav) or []
    s03_breaches = S03_vm_section(date, fund, section, icon, nav=nav) or []

    return s01_breaches + s02_breaches + s03_breaches


def S01_simm_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = None,

        section : str = "VaR/SIMM",
        icon : str = "📈",

        title : str = "SIMM",
        risk : str = "S01",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

        nav : float = 1.0,

    ) :
    """
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, real_date = get_simm_nav_changes_from_date(date=date, fund=fund, nav_value=nav)

    margin_line()

    if dataframe is not None and not dataframe.is_empty() :

        simm_value = dataframe["Current Value / NAV (%)"][0]
        st.markdown(simm_colored_card(simm_value, real_date), unsafe_allow_html=True)
        render_changes_table(
            dataframe,
            title="SIMM data and changes",
            date=real_date,
            rename_columns=_changes_table_rename_columns(),
            hide_columns=_changes_table_hide_columns(hide_simm_pct=True),
        )

    else :

        st.write("No SIMM data available.")

    return None


def S02_im_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        title : str = "IM",
        risk : str = "S02",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

        nav : float = 1.0
    ) :
    """
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    col1, col2 = st.columns(2)

    with col1 :
        
        margin_line()
        im_ctpy_section(date, fund, nav=nav)

    with col2 :

        margin_line()
        im_ice_section(date, fund, nav=nav)

    return None


def im_ctpy_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = None,

        nav : Optional[float] = 1.0,
        rename_map : Optional[Dict] = None,

    ) :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund)

    
    fig = plot_im_by_bank(dataframe, md5, nav_value=nav, title="IM Over Time by Counterparty (Data)")
    render_plotly_chart(fig)

    changes_dataframe, real_date = get_im_ctpy_changes_from_date(dataframe, md5, date, fund, nav_value=nav)
    render_changes_table(
        changes_dataframe,
        title="IM counterparty data and changes",
        date=real_date,
        rename_columns=_changes_table_rename_columns(),
        hide_columns=_changes_table_hide_columns(),
    )

    margin_line()

    return None


def im_ice_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = None,

        nav : Optional[float] = 1.0,
        rename_map : Optional[Dict] = None,

    ) :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    rename_map = RENAME_COUNTERPARTY_MAP if rename_map is None else rename_map

    dataframe, md5  = get_im_ice_all_history(date, fund)

    fig = plot_im_by_bank(
        dataframe, md5,
        bank_col="Counterparty",
        nav_value=nav,
        alias_map=rename_map,
        title="IM Over Time by Counterparty (ICE)"
    
    )


    render_plotly_chart(fig)

    changes_dataframe, real_date = get_im_ice_changes_from_date(dataframe, md5, date, fund, nav_value=nav, rename_map=rename_map)
    render_changes_table(
        changes_dataframe,
        title="IM ICE data and changes",
        date=real_date,
        rename_columns=_changes_table_rename_columns(),
        hide_columns=_changes_table_hide_columns(),
    )

    return None


def S03_vm_section (
        
        date : Optional[str | dt.date | dt.datetime] = None,
        fund : Optional[str] = "HV",

        section : str = "VaR/SIMM",
        icon : str = "📈",

        title : str = "VM",
        risk : str = "S03",

        path_by_fund : Optional[Dict[str]] = None,
        style : str = subsections_controls_style,

        nav : float = 1.0
    ) :
    """
    """
    st.markdown(f'{style}<div class="section-title">{icon} {section} - {title} ({risk})</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1 :

        margin_line()
        vm_ctpy_section(date, fund, nav=nav)
    
    with col2 :

        margin_line()
        vm_ice_section(date, fund, nav=nav)

    return None


def vm_ctpy_section (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav : Optional[float] = 1.0,
        rename_map : Optional[Dict] = None,

    ) -> None :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5  = get_vm_ctpy_all_history(date, fund)

    fig = plot_vm_by_bank(dataframe, md5, bank_col="Bank", value_col="VM", nav_value=nav, title="VM Over Time by Counterparty (Data)")
    render_plotly_chart(fig)

    changes_dataframe, real_date = get_vm_ctpy_changes_from_date(dataframe, md5, date, fund, nav_value=nav)
    render_changes_table(
        changes_dataframe,
        title="VM counterparty data and changes",
        date=real_date,
        rename_columns=_changes_table_rename_columns(),
        hide_columns=_changes_table_hide_columns(),
    )

    return None


def vm_ice_section (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav : Optional[float] = 1.0,
        rename_map : Optional[Dict] = None,
    
    ) -> None :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    rename_map = RENAME_COUNTERPARTY_MAP if rename_map is None else rename_map

    dataframe, md5  = get_vm_ice_all_history(date, fund)

    fig = plot_vm_by_bank(dataframe, md5, bank_col="Counterparty", value_col="MV", nav_value=nav, alias_map=rename_map, title="VM Over Time by Counterparty (ICE)")
    render_plotly_chart(fig)

    changes_dataframe, real_date = get_vm_ice_changes_from_date(dataframe, md5, date, fund, nav_value=nav, rename_map=rename_map)
    render_changes_table(
        changes_dataframe,
        title="VM ICE data and changes",
        date=real_date,
        rename_columns=_changes_table_rename_columns(),
        hide_columns=_changes_table_hide_columns(),
    )

    return None


def _changes_table_rename_columns () -> Dict[str, str] :
    """
    Columns renamed for SIMM/IM/VM changes display.
    """
    return {"Current Value / NAV (%)" : "SIMM %"}


def _changes_table_hide_columns (
        
        hide_simm_pct : bool = False,

    ) -> List[str] :
    """
    Columns kept out of the table because they are shown in the title.
    """
    columns = ["Real Date"]

    if hide_simm_pct :
        columns.append("Current Value / NAV (%)")

    return columns
