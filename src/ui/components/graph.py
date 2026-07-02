from __future__ import annotations

import streamlit as st
import polars as pl
import plotly.graph_objects as go

from typing import Optional, List, Tuple, Dict

from src.utils.logger import log


def render_plotly_chart (
        
        fig : Optional[go.Figure] = None,

    ) -> None :
    """
    Render a Plotly chart when data is available.
    """
    if fig is None :

        st.write("No chart data available.")
        return None

    st.plotly_chart(fig, width="content")

    return None


def plot_im_by_bank (
        
        _dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        x_axis : str = "Date",
        bank_col : str = "Bank",
        value_col : str = "IM",
        nav_value : Optional[float] = 1.0,
        
        alias_map : Optional[dict[str, str]] = None,
        
        title : Optional[str] = "Initial Margin over time by counterparty",
        height : int = 450,
        width : Optional[int] = None,
    
    ) -> Optional[go.Figure]:
    """
    
    """
    if _dataframe is None or _dataframe.is_empty() :
        return None

    missing = [c for c in (x_axis, bank_col, value_col) if c not in _dataframe.columns]
    
    if missing :

        log(f"Missing columns: {missing}")
        return None

    pct_mode = st.radio("Display mode", ["Raw values", "Percentage"], horizontal=True, key=f"im_display_mode_{md5}") == "Percentage"

    if pct_mode and not nav_value :

        log("A non-zero NAV value is required for percentage view.")
        return None

    df, yaxis_title, hover_suffix = _prepare_im_vm_data(_dataframe, md5, x_axis, bank_col, value_col, nav_value or 1.0, pct_mode, alias_map)

    fig = go.Figure(

        [
            go.Scatter(
                
                x=sub[x_axis].to_list(),
                y=sub["_y"].to_list(),
                mode="lines", name=str(bank), line_shape="spline", connectgaps=True,
                hovertemplate=f"<b>{bank}</b><br>{x_axis}: %{{x}}<br>{yaxis_title}: %{{y:,.2f}}{hover_suffix}<extra></extra>",
            )

            for bank in df[bank_col].unique().sort().to_list()
            for sub in [df.filter(pl.col(bank_col) == bank)]
        ]
    
    )

    axis = dict(showgrid=True, title_font=dict(size=18), tickfont=dict(size=13))
    
    fig.update_layout(

        title=title,
    
        hovermode="x unified",
        template="plotly_white",
    
        height=height,
        margin=dict(l=0, r=0, t=40, b=0),
        
        xaxis=dict(title=x_axis, **axis),
        yaxis=dict(title=yaxis_title, **axis),
        
        hoverlabel=dict(bgcolor="white",font_color="black", font_size=16),
        legend=dict(title="Bank", y=0.5, yanchor="middle"), **({"width": width} if width else {}),
    
    )
    
    fig.update_yaxes(ticksuffix=hover_suffix, tickformat=".2f" if pct_mode else ",.0f")

    return fig


def plot_vm_by_bank(

        _dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        x_axis: str = "Date",
        bank_col: str = "Bank",
        value_col: str = "VM",

        nav_value : Optional[float] = 1.0,
        alias_map : Optional[dict[str, str]] = None,

        title : Optional[str] = "Variation Margin over time by counterparty",
        height : int = 450,
        width : Optional[int] = None,

    ) -> Optional[go.Figure] :
    """
    Plot VM by bank, mirroring plot_im_by_bank.
    """

    if _dataframe is None or _dataframe.is_empty():
        return None

    missing = [c for c in (x_axis, bank_col, value_col) if c not in _dataframe.columns]

    if missing :

        log(f"Missing columns: {missing}")
        return None

    pct_mode = st.radio("Display mode", ["Raw values", "Percentage"], horizontal=True, key=f"vm_display_mode_{md5}") == "Percentage"

    if pct_mode and not nav_value :

        log("A non-zero NAV value is required for percentage view.")
        return None

    df, yaxis_title, hover_suffix = _prepare_im_vm_data(
    
        _dataframe, md5, x_axis, bank_col, value_col,
        nav_value or 1.0, pct_mode, alias_map
    
    )

    fig = go.Figure(
        [
            go.Scatter(
            
                x=sub[x_axis].to_list(),
                y=sub["_y"].to_list(),
                mode="lines", name=str(bank), line_shape="spline", connectgaps=True,
                hovertemplate=(
                    f"<b>{bank}</b><br>{x_axis}: %{{x}}<br>"
                    f"{yaxis_title}: %{{y:,.2f}}{hover_suffix}<extra></extra>"
                ),
            
            )
            
            for bank in df[bank_col].unique().sort().to_list()
            for sub in [df.filter(pl.col(bank_col) == bank)]
        ]
    
    )

    axis = dict(showgrid=True, title_font=dict(size=18), tickfont=dict(size=13))

    fig.update_layout(
        title=title,
        hovermode="x unified",
        template="plotly_white",
        height=height,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(title=x_axis, **axis),
        yaxis=dict(title=yaxis_title, **axis),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=16),
        legend=dict(title="Bank", y=0.5, yanchor="middle"),
        **({"width": width} if width else {}),
    )

    fig.update_yaxes(ticksuffix=hover_suffix, tickformat=".2f" if pct_mode else ",.0f")

    return fig


@st.cache_data()
def plot_nav_dataframe(

        _dataframe: Optional[pl.DataFrame] = None,
        md5: Optional[str] = None,
        title: str = "NAV over time",

        x_axis: str = "date",
        xaxis_title: str = "Date",
        metrics: Optional[List[str]] = ["NAV Estimate"],
        yaxis_title: str = "NAV Estimate",
        tickformat: str = ",.0f",

        height: int = 450,
        width: Optional[int] = None,
        rename_metrics: Optional[Dict[str, str]] = None,
    
    ) -> Optional[go.Figure]:
    """
    Plot NAV series from a prepared dataframe.
    """
    if _dataframe is None or _dataframe.is_empty():
    
        st.cache_data.clear()
    
        log("[-] No NAV dataframe available", "error")
        return None
    
    if not metrics :
    
        log("[-] No NAV columns provided to plot", "error")
        return None

    missing = [column for column in [x_axis, *metrics] if column not in _dataframe.columns]
    
    if missing:
        log(f"[-] Missing NAV columns: {missing}", "error")
        return None

    dataframe = _dataframe.drop_nulls(subset=[x_axis]).sort(x_axis)
    if dataframe.is_empty():
        return None

    rename_metrics = rename_metrics or {}

    fig = go.Figure()
    for column in metrics:
        sub = dataframe.drop_nulls(subset=[column])
        if sub.is_empty():
            continue

        display_name = rename_metrics.get(column, column)

        fig.add_trace(
            go.Scatter(
                x=sub[x_axis].to_list(),
                y=sub[column].to_list(),
                mode="lines",
                name=display_name,
                line_shape="spline",
                connectgaps=True,
                hovertemplate=(
                    f"<b>{display_name}</b><br>{xaxis_title}: %{{x}}<br>"
                    f"{yaxis_title}: %{{y:,.2f}}<extra></extra>"
                ),
            )
        )

    if len(fig.data) == 0:
        return None

    axis = dict(showgrid=True, title_font=dict(size=18), tickfont=dict(size=13))
    fig.update_layout(
        title=title,
        hovermode="x unified",
        template="plotly_white",
        height=height,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(title=xaxis_title, **axis),
        yaxis=dict(title=yaxis_title, **axis),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=16),
        legend=dict(title="Metric", y=0.5, yanchor="middle"),
        **({"width": width} if width else {}),
    )
    fig.update_yaxes(tickformat=tickformat)
    return fig

@st.cache_data
def _prepare_im_vm_data (

        _dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        x_axis: str = "Date",
        bank_col: str = "Bank",
        value_col: str = "IM",
        
        nav_value : Optional[float] = 1.0,
    
        pct_mode : bool = True,
        alias_map : Optional[dict[str, str]] = None,
    
    ) -> tuple[pl.DataFrame, str, str]:
    """
    
    """
    if _dataframe is None :

        st.cache_data.clear()
        return None
    
    if alias_map :
        _dataframe = _dataframe.with_columns(pl.col(bank_col).replace(alias_map))

    expr = ((pl.col(value_col) / nav_value) * 100) if pct_mode else pl.col(value_col)
    yaxis_title = f"{value_col} / NAV (%)" if pct_mode else value_col

    data = (

        _dataframe.with_columns(expr.alias("_y")).sort([bank_col, x_axis]),
        yaxis_title,
        "%" if pct_mode else "",

    )

    return data 
