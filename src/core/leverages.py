from __future__ import annotations

import os
import polars as pl
import datetime as dt

from typing import Optional, Dict, List, Any

from src.config.parameters import (
    AEGIS_DISC_FUND_HV,
    AEGIS_LEVERAGES_ALL_SCHEMA_OVERRIDES,
    AEGIS_LEVERAGES_ALL_COLUMNS_SCHEMA_OVERRIDES
)
from src.config.paths import (
    AEGIS_LEVERAGES_ALL_FILENAME,
    AEGIS_LEVERAGES_FUNDS_DIR_PATHS,
    AEGIS_LEVERAGES_TRADE_FUNDS_DIR_PATHS,
    AEGIS_LEVERAGES_UNDERL_FUNDS_DIR_PATHS
)

from src.utils.logger import log
from src.utils.date import (
    get_ytd_bussiness_day, get_qtd_bussiness_day, get_1m_bussiness_day,
    get_1w_bussiness_day, get_previous_bussiness_day  
)
from src.utils.formatter import str_to_date, date_to_str, str_to_datetime
from src.utils.data_io import load_excel_to_dataframe


def get_historical_leverage (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        paths_by_funds : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        date_column : Optional[str] = "Date"

    ) :
    
    """
    
    """
    date = str_to_datetime(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    paths_by_funds = AEGIS_LEVERAGES_FUNDS_DIR_PATHS if paths_by_funds is None else paths_by_funds
    dir_abs_path = paths_by_funds.get(fund, None)

    if dir_abs_path is None or not os.path.exists(dir_abs_path) :

        log("Leverage directory not found. Please update the ENV variables.")
        return None

    filename = AEGIS_LEVERAGES_ALL_FILENAME if filename is None else filename
    file_abs_path = os.path.join(dir_abs_path, filename)

    if file_abs_path is None or not os.path.exists(file_abs_path) :
        
        log("Historical Leverage file does not exists.")
        return None
    
    schema_overrides = AEGIS_LEVERAGES_ALL_SCHEMA_OVERRIDES if schema_overrides is None else schema_overrides
    
    dataframe, md5 = load_excel_to_dataframe(
    
        file_abs_path,
        schema_overrides=schema_overrides,
        specific_cols=list(schema_overrides.keys())
    
    )

    if dataframe is None :

        log("Leverage dataframe is Null or does not exists.")
        return None
    
    dataframe = dataframe.filter(pl.col(date_column) <= date)
    dataframe = dataframe.drop_nulls()

    print(dataframe)

    return dataframe, md5


def update_historical_leverage (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        path_by_fund : Optional[Dict] = None,

    ) :
    """
    
    """
    response = {

        "sucess" : False,
        "log" : None,

    }


    date = str_to_date(date)
    fund = "HV" if fund is None else fund

    path_by_fund = None if path_by_fund is None else path_by_fund
    file_abs_path = path_by_fund.get(fund, None)

    if file_abs_path is None or not os.path.exists(file_abs_path) :
        return response

    return None


def get_leverage_changes_from_date (
        
        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        schema_overrides : Optional[Dict] = None,
        date_column : str = "Date",

    ) -> Optional[pl.DataFrame] :
    """
    
    """
    date = str_to_datetime(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    schema_overrides = AEGIS_LEVERAGES_ALL_SCHEMA_OVERRIDES if schema_overrides is None else schema_overrides
    dataframe, md5 = get_historical_leverage(date, fund, schema_overrides=schema_overrides) if dataframe is None else (dataframe, md5)

    if dataframe is None :

        log("No historical leverages dataframe avaialble.")
        return None
    
    columns_values : List[str] = [column for column in dataframe.columns if column != date_column]

    if columns_values is None or len(columns_values) == 0 :
        
        log("No Leverage metrics availables. Retry or update your files")
        return None
    
    dataframe = (dataframe.drop_nulls(subset=[date_column])
        .with_columns(pl.col(date_column).cast(pl.Datetime("ms")))
        .filter(pl.col(date_column) <= date)
        .sort(date_column)
    )

    if dataframe.is_empty() :

        log("No historical leverage data available before or at the requested date.")
        return None

    current_row = dataframe.tail(1)
    dates_to_check = _build_reference_dates_dataframe(date)

    matched = dates_to_check.join_asof(
    
        dataframe,
        left_on="Check Date",
        right_on=date_column,
        strategy="backward",
    
    )

    if matched.is_empty() :

        log("No matching historical leverage data found for reference dates.")
        return None

    df = _build_leverage_changes_output(current_row=current_row, matched=matched, columns_values=columns_values)
    
    return df


def _build_reference_dates_dataframe (
        
        date : Optional[str | dt.date | dt.datetime] = None

    ) -> Optional[pl.DataFrame] :
    """
    Build reference dates used to compute leverage changes.
    """

    reference_dates = {
    
        "1D Change (%)": get_previous_bussiness_day(date),
        "1W Change (%)": get_1w_bussiness_day(date),
        "1M Change (%)": get_1m_bussiness_day(date),
        "QTD Change (%)": get_qtd_bussiness_day(date),
        "YTD Change (%)": get_ytd_bussiness_day(date),
    
    }

    rows = [
        {
            "Label": label,
            "Check Date": _date_to_datetime_ms(check_date),
            "Display Order": index,
        }
        for index, (label, check_date) in enumerate(reference_dates.items())
    ]

    reference_df = (

        pl.DataFrame(rows)
        .with_columns(
            pl.col("Check Date").cast(pl.Datetime("ms"))
        )
        .sort("Check Date")
    )

    return reference_df 


def _date_to_datetime_ms(value: dt.date | dt.datetime) -> dt.datetime:
    """
    Normalize a Python date/datetime to a datetime.

    Polars needs homogeneous values when building a Datetime column.
    """
    if isinstance(value, dt.datetime):
        return value.replace(hour=0, minute=0, second=0, microsecond=0)

    return dt.datetime.combine(value, dt.time.min)


def _build_leverage_changes_output (
        
        current_row : Optional[pl.DataFrame] = None,
        matched : Optional[pl.DataFrame] = None,
        columns_values : Optional[List[str]] = None,
    
    ) -> Optional[pl.DataFrame] :
    """
    Build final transposed output:

    Metric | Current Value | 1D Change (%) | 1W Change (%) | ...
    """
    matched_rows = {

        row["Label"]: row
        for row in matched.to_dicts()
    
    }

    rows = []

    for metric in columns_values :
    
        current_value = current_row[metric][0]

        row = {

            "Metric": metric,
            "Current Value": current_value,
        
        }

        for label, matched_row in matched_rows.items() :
        
            historical_value = matched_row.get(metric)
            row[label] = _compute_change_pct(current_value, historical_value)

        rows.append(row)

    return pl.DataFrame(rows)


def _compute_change_pct (
        
        current_value : Optional[float | int] = None,
        historical_value : Optional[float | int]  = None,

    ) -> Optional[float] :
    """
    Compute percentage change between current and historical value.
    """
    if current_value is None :
        return None

    if historical_value is None or historical_value == 0 :
        return None

    change_pct = ((current_value - historical_value) / historical_value) * 100 
    
    return change_pct 



def get_last_row_before (ref_date : Optional[str | dt.date | dt.datetime] = None) :
    """
    
    """