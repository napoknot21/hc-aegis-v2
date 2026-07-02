from __future__ import annotations

import os
import polars as pl
import datetime as dt

from typing import Optional, Dict, Any, List, Tuple


from src.config.parameters import AEGIS_DISC_FUND_HV, AEGIS_SIMM_CUTOFF_DATE, AEGIS_NAV_ESTIMATE_HISTORY_SCHEMA_OVERRIDES
from src.config.paths import AEGIS_NAV_ESTIMATE_FILENAME, AEGIS_NAV_ESTIMATE_FUNDS_DIR_PATH
from src.core.data.simm._common import _get_changes_from_date
from src.utils.formatter import str_to_date, str_to_datetime
from src.utils.date import today_previous_bussiness_day, today_next_bussiness_day
from src.utils.data_io import load_excel_to_dataframe
from src.utils.logger import log


def get_nav_estimate_all_history_raw (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        path_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        inception_date : Optional[str | dt.datetime | dt.date] = None,


    ) -> tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_datetime(None)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    filename = AEGIS_NAV_ESTIMATE_FILENAME if filename is None else filename
    path_by_fund = AEGIS_NAV_ESTIMATE_FUNDS_DIR_PATH if path_by_fund is None else path_by_fund

    dir_abs_path = path_by_fund.get(fund, None)

    if dir_abs_path is None or not os.path.exists(dir_abs_path) :

        log(f"NAV estimated history directory not found for fund: {fund} and date: {date}")
        return None, None
    
    file_abs_path = os.path.join(dir_abs_path, filename)

    if file_abs_path is None or not os.path.exists(file_abs_path) :

        log(f"NAV estimated history file not found for fund: {fund} and date: {date}")
        return None, None
    
    schema_overrides = AEGIS_NAV_ESTIMATE_HISTORY_SCHEMA_OVERRIDES if schema_overrides is None else schema_overrides
    columns = list(schema_overrides.keys()) if schema_overrides is not None else None

    dataframe, md5 = load_excel_to_dataframe(file_abs_path, schema_overrides=schema_overrides, specific_cols=columns)

    if dataframe is None :

        log(f"No NAV estimated history data found for fund: {fund} and date: {date}")
        return None, None
      
    return dataframe, md5


def get_nav_estimate_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        path_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        inception_date : Optional[str | dt.datetime | dt.date] = None,

        date_column : Optional[str] = "date",

    ) -> tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_datetime(date, mode="max")
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    filename = AEGIS_NAV_ESTIMATE_FILENAME if filename is None else filename
    path_by_fund = AEGIS_NAV_ESTIMATE_FUNDS_DIR_PATH if path_by_fund is None else path_by_fund

    schema_overrides = AEGIS_NAV_ESTIMATE_HISTORY_SCHEMA_OVERRIDES if schema_overrides is None else schema_overrides
    inception_date = str_to_datetime(AEGIS_SIMM_CUTOFF_DATE) if inception_date is None else inception_date
    
    dataframe, md5 = get_nav_estimate_all_history_raw(date, fund, filename, path_by_fund, schema_overrides, inception_date)
    
    if dataframe is None :

        log(f"No NAV estimated history data found for fund: {fund} and date: {date}")
        return None, None

    dataframe = dataframe.filter(pl.col(date_column) >= inception_date)
    dataframe = dataframe.filter(pl.col(date_column) <= date)
    
    return dataframe, md5


def get_nav_estimate_values_by_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        schema_overrides : Optional[Dict] = None,
        date_column : Optional[str] = "date",
 
    ) -> tuple[Optional[pl.DataFrame], Optional[str], Optional[str | dt.datetime | dt.date]] :
    """
    
    """
    date = str_to_datetime(date, mode="max")
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_nav_estimate_all_history(date, fund, schema_overrides=schema_overrides) if dataframe is None else (dataframe, md5)

    if dataframe is None :

        log(f"No NAV estimated history data found for fund: {fund} and date: {date}")
        return None, None, None

    buiness_date = str_to_datetime(today_previous_bussiness_day(date), mode="min")
    dataframe_exact = (dataframe.filter(pl.col(date_column).dt.date() == buiness_date.date()).top_k(1, by=date_column))

    if not dataframe_exact.is_empty() :
        
        found_date = dataframe_exact[date_column][0]
        return dataframe_exact, md5, found_date

    dataframe = dataframe.filter(pl.col(date_column) <= buiness_date).sort(date_column)

    if dataframe.is_empty() :
        
        log(f"No NAV estimated values found for fund: {fund} and business date: {buiness_date}")
        return None, None, None

    dataframe = dataframe.tail(1)
    found_date = dataframe[date_column][0]

    return dataframe, md5, found_date


# ---------------- formatters ----------------

def convert_nav_estimate_history_to_base100 (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        inception_date : Optional[str | dt.datetime | dt.date] = None,
        schema_overrides : Optional[Dict] = None,

        date_column : Optional[str] = "date",
        metrics : Optional[Tuple[str]] = ("NAV Estimate",)

    ) -> tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_nav_estimate_all_history(date, fund, schema_overrides=schema_overrides) if dataframe is None else (dataframe, md5)

    if dataframe is None :
        return None, None
    
    inception_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if inception_date is None else inception_date)
    
    missing_metrics = [metric for metric in metrics if metric not in dataframe.columns]

    if missing_metrics :

        log(f"Column(s) {missing_metrics} not found in NAV estimated history for fund: {fund}")
        return None, None
    
    dataframe = dataframe.drop_nulls(subset=list(metrics))

    if dataframe.is_empty() :

        log(f"No valid (non-null) NAV estimated data found for fund: {fund}")
        return None, None

    inception_row, _ = get_nav_estimate_values_by_date(
    
        dataframe=dataframe,
        md5=md5,
        date=inception_date,
        fund=fund,
        date_column=date_column,
    
    )

    if inception_row is None or inception_row.is_empty() :
        inception_row = dataframe.sort(date_column).head(1)

    if inception_row is None or inception_row.is_empty() :
        log(f"No inception row available for NAV estimated data for fund: {fund}")
        return None, None

    dataframe = dataframe.with_columns(
    
        [
            (pl.col(metric) / inception_row.select(metric).item() * 100)
            .alias(f"{metric}_base100")
            for metric in metrics
        ]
    
    )
    

    return dataframe, md5


def get_nav_estimate_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        nav_value : Optional[float] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Compute NAV estimate changes from history.
    """
    date = str_to_datetime(date, mode="max")
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    df_date, md5_date, real_date = get_nav_estimate_values_by_date(dataframe, md5, date, fund)

    dataframe, md5 = get_nav_estimate_all_history(date, fund) if dataframe is None else (dataframe, md5)

    return _get_changes_from_date(

        dataframe=dataframe,
        date=date,
        value_col="NAV Estimate",
        group_col=None,
        metric_name="NAV Estimate",
        nav_value=nav_value,
    
    )


def rename_nav_estimate_columns (

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        rename_map : Optional[Dict] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[dt.date]] :
    """
    Rename NAV estimate columns based on a provided mapping.
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_nav_estimate_all_history(date, fund) if dataframe is None else (dataframe, md5)

    if dataframe is None :

        log(f"No NAV estimated history data found for fund: {fund} and date: {date}")
        return None, None

    rename_map = {} if rename_map is None else rename_map
    dataframe = dataframe.rename(rename_map)

    return dataframe, md5


# ---------------- Updaters ----------------


def update_nav_estimate_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        path_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        inception_date : Optional[str | dt.datetime | dt.date] = None,


    ) -> tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    return None, None


# ---------------- functions to chen ----------------
