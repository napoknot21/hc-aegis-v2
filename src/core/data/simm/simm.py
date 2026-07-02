from __future__ import annotations

import datetime as dt
import polars as pl

from typing import Optional, Dict, Tuple

from src.config.parameters import AEGIS_DISC_FUND_HV, AEGIS_IM_ICE_COLUMNS, AEGIS_SIMM_CUTOFF_DATE
from src.config.paths import AEGIS_IM_ICE_FILE, AEGIS_IM_ICE_FUNDS_DIR_PATH
from src.core.data.simm._common import _get_changes_from_date, _read_all_history
from src.utils.formatter import str_to_date


def get_simm_history (

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    Read the ICE IM history used as the SIMM source.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    filename = AEGIS_IM_ICE_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_ICE_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    schema_overrides = AEGIS_IM_ICE_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    return _read_all_history(date, fund, filename, paths_by_fund, schema_overrides, cutoff_date)


def get_simm_nav_changes_from_date (

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute total ICE IM changes used for the SIMM/NAV control.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_simm_history(date, fund) if dataframe is None else (dataframe, md5)

    return get_simm_changes_from_date(
        dataframe=dataframe,
        md5=md5,
        date=date,
        fund=fund,
        value_col="IM",
        group_col=None,
        metric_name="SIMM",
        nav_value=nav_value,
        change_mode="nav_pct_point",
    )


def get_simm_changes_from_date (

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        value_col : str = "IM",
        group_col : Optional[str] = "Bank",
        date_column : str = "Date",
        metric_name : Optional[str] = None,

        nav_value : Optional[float] = None,
        alias_map : Optional[Dict] = None,
        change_mode : str = "relative_pct",

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute current value and 1D/1M/YTD changes from SIMM-family history.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    return _get_changes_from_date(
        dataframe=dataframe,
        date=date,
        value_col=value_col,
        group_col=group_col,
        date_column=date_column,
        metric_name=metric_name,
        nav_value=nav_value,
        alias_map=alias_map,
        change_mode=change_mode,
    )
