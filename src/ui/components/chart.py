from __future__ import annotations

import polars as pl
import datetime as dt

import streamlit as st
import plotly.graph_objects as go

from typing import Any, Optional, List

from src.utils.logger import log
from src.utils.formatter import str_to_date




@st.cache_data()
def leverage_line_chart (
        
        _dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,
        
        title : str = "Leverage over time",
        date : Optional[str | dt.datetime | dt.date] = None,
        
        columns : Optional[List[str]] = None,
        x_axis : Optional[str] = "Date",
        background_ranges : Optional[List[dict[str, Any]]] = None,

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
    y_values_by_column: dict[str, list[Any]] = {}

    # Plot using Plotly
    fig = go.Figure()

    for column in columns :

        if column not in df.columns :

            log(f"[-] Column '{column}' not in dataframe", "warning")
            continue
        
        y_values = df.get_column(column).to_list()
        y_values_by_column[column] = y_values

        fig.add_trace(

            go.Scatter(
            
                x=x_values,
                y=y_values,
                mode="lines",
                name=column,
                line_shape="spline",
            
            )

        )

    if background_ranges :

        numeric_values = []
        
        for values in y_values_by_column.values():
            
            for value in values :

                if value is None:
                    continue

                try:
                    numeric_values.append(float(value))
                
                except (TypeError, ValueError):
                    continue

        min_y = min(numeric_values, default=0)
        max_y = max(numeric_values, default=0)
        range_bounds = [
            value
            for item in background_ranges
            for value in (item.get("from"), item.get("to"))
            if value is not None
        ]
        y_lower = min([min_y, *range_bounds])
        y_upper = max([max_y, *range_bounds]) * 1.05

        for item in background_ranges :

            if not item.get("color") :
                continue
            
            y0 = y_lower if item.get("from") is None else item["from"]
            y1 = y_upper if item.get("to") is None else item["to"]

            fig.add_hrect(
                y0=y0,
                y1=y1,
                fillcolor=item["color"],
                opacity=0.16 if item.get("opacity") is None else item["opacity"],
                line_width=0,
                layer="below",
            )

        fig.update_yaxes(range=[y_lower, y_upper])

        
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
