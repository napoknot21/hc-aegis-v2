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

    {
        "Current" : pl.Float64,
        "1D Change (%)" : pl.Float64,
        "1W Change (%)" : pl.Float64,
        "1M Change (%)" : pl.Float64,
        "QTD Change (%)" : pl.Float64,
        "YTD Change (%)" : pl.Float64,
    }


    print(columns_values)
    
    return None



