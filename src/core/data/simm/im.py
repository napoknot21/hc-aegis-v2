from __future__ import annotations

import datetime as dt
import polars as pl

from typing import Optional, Dict, Tuple

from src.config.parameters import (
    AEGIS_DISC_FUND_HV,
    AEGIS_IM_CTPY_COLUMNS,
    AEGIS_IM_ICE_COLUMNS,
    AEGIS_SIMM_CUTOFF_DATE,
)
from src.config.paths import (
    AEGIS_IM_CTPY_FILE,
    AEGIS_IM_CTPY_FUNDS_DIR_PATH,
    AEGIS_IM_ICE_FILE,
    AEGIS_IM_ICE_FUNDS_DIR_PATH,
)
from src.core.data.simm._common import _get_changes_from_date, _get_values_by_date, _read_all_history
from src.utils.formatter import str_to_date


def get_im_ctpy_all_history (

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    Read all counterparty IM history available up to the requested date.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    filename = AEGIS_IM_CTPY_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_CTPY_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    return _read_all_history(date, fund, filename, paths_by_fund, schema_overrides, cutoff_date)


def get_im_ice_all_history (

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    Read all ICE IM history available up to the requested date.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    filename = AEGIS_IM_ICE_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_ICE_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    schema_overrides = AEGIS_IM_ICE_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    return _read_all_history(date, fund, filename, paths_by_fund, schema_overrides, cutoff_date)


def get_im_ctpy_values_by_date (

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        schema_overrides : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str], Optional[dt.date]] :
    """
    Return counterparty IM rows for the latest available date.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund) if dataframe is None else (dataframe, md5)
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides

    values_dataframe, available_date = _get_values_by_date(dataframe, date, schema_overrides)

    if dataframe is None :
        return None, None, None

    return values_dataframe, md5 if available_date is not None else None, available_date


def get_im_ice_values_by_date (

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        schema_overrides : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str], Optional[dt.date]] :
    """
    Return ICE IM rows for the latest available date.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ice_all_history(date, fund) if dataframe is None else (dataframe, md5)
    schema_overrides = AEGIS_IM_ICE_COLUMNS if schema_overrides is None else schema_overrides

    values_dataframe, available_date = _get_values_by_date(dataframe, date, schema_overrides)

    if dataframe is None :
        return None, None, None

    return values_dataframe, md5 if available_date is not None else None, available_date


def get_im_ctpy_changes_from_date (

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute IM changes from counterparty data history.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund) if dataframe is None else (dataframe, md5)

    return _get_changes_from_date(
        dataframe=dataframe,
        date=date,
        value_col="IM",
        group_col="Bank",
        nav_value=nav_value,
    )


def get_im_ice_changes_from_date (

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,
        rename_map : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute IM changes from ICE history.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ice_all_history(date, fund) if dataframe is None else (dataframe, md5)

    return _get_changes_from_date(
        dataframe=dataframe,
        date=date,
        value_col="IM",
        group_col="Counterparty",
        nav_value=nav_value,
        alias_map=rename_map,
    )
