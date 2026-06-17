from __future__ import annotations

import polars as pl
import datetime as dt

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from typing import Optional, List

from src.utils.logger import log
from src.utils.formatter import str_to_date




@st.cache_data()
def leverage_line_chart (
        
        _dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,
        
        title : str = "Leverage over time",
        date : Optional[str | dt.datetime | dt.date] = None,
        
        columns : Optional[List[str]] = None,
        x_axis : Optional[str] = "Date"

    ) :
    """
    
    """
    if _dataframe is None :

        st.cache_data.clear()
        log("[-] No Dataframe available", "error")

        return None
    
    if not columns :
        
        st.cache_data.clear()
        log("[-] No columns provided to plot", "error")
        
        return None

    date = str_to_date(date)

    df = _dataframe.sort(x_axis)
    df = df.filter(
        pl.any_horizontal([pl.col(c).is_not_null() for c in columns])
    )
    df = df.filter(pl.col(x_axis) <= pl.lit(date))

    x_values = df.get_column(x_axis).to_list()

    # Plot using Plotly
    fig = go.Figure()

    for column in columns :

        if column not in df.columns :

            log(f"[-] Column '{column}' not in dataframe", "warning")
            continue
        
        y_values = df.get_column(column).to_list()

        fig.add_trace(

            go.Scatter(
            
                x=x_values,
                y=y_values,
                mode="lines",
                name=column,
                line_shape="spline",
            
            )

        )

        
    fig.update_layout(

        title=title,
        
        xaxis=dict(title=x_axis),
        yaxis=dict(title="Leverages"),
        
        hovermode="x unified",
        
        hoverlabel=dict(
            bgcolor="white",
            font_color="black",
            font_size=16,
        ),

        legend=dict(
            y=0.5,
            yanchor="middle"
        ),
    )
        
    return fig
