from __future__ import annotations

import polars as pl
import datetime as dt
import streamlit as st

from typing import Optional, Dict, List

from src.utils.formatter import date_to_str


def render_changes_table (
        
        dataframe : Optional[pl.DataFrame] = None,

        title : Optional[str] = None,
        date : Optional[str | dt.datetime | dt.date] = None,

        rename_columns : Optional[Dict[str, str]] = None,
        hide_columns : Optional[List[str]] = None,

        round_value : int = 2,

    ) -> None :
    """
    Render a generic changes dataframe with an optional dated title.
    """
    if dataframe is None or dataframe.is_empty() :

        st.write("No changes data available.")
        return None

    dataframe = prepare_changes_table_dataframe(dataframe, rename_columns, hide_columns, round_value)

    if title is not None :
        st.markdown(f"**{_build_changes_table_title(title, date)}**")

    st.dataframe(dataframe, hide_index=True)

    return None


def prepare_changes_table_dataframe (
        
        dataframe : Optional[pl.DataFrame] = None,
        rename_columns : Optional[Dict[str, str]] = None,
        hide_columns : Optional[List[str]] = None,
        round_value : int = 2,

    ) -> Optional[pl.DataFrame] :
    """
    Prepare a dataframe for display without changing the source object.
    """
    if dataframe is None :
        return None

    hide_columns = [] if hide_columns is None else hide_columns
    rename_columns = {} if rename_columns is None else rename_columns

    columns_to_drop = [column for column in hide_columns if column in dataframe.columns]

    if columns_to_drop :
        dataframe = dataframe.drop(columns_to_drop)

    rename_columns = {
        old_name : new_name
        for old_name, new_name in rename_columns.items()
        if old_name in dataframe.columns
    }

    if rename_columns :
        dataframe = dataframe.rename(rename_columns)

    float_columns = [
        column
        for column, dtype in dataframe.schema.items()
        if dtype in (pl.Float32, pl.Float64)
    ]

    if float_columns :
        dataframe = dataframe.with_columns([pl.col(column).round(round_value) for column in float_columns])

    return dataframe


def _build_changes_table_title (
        
        title : str,
        date : Optional[str | dt.datetime | dt.date] = None,

    ) -> str :
    """
    Append a normalized date to the table title when available.
    """
    if date is None :
        return title

    return f"{title} at {date_to_str(date)}"

