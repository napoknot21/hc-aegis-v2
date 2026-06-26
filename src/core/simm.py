from __future__ import annotations

import os
import polars as pl
import datetime as dt

from typing import Optional, Dict, List, Tuple

from src.utils.logger import log
from src.config.parameters import (
    AEGIS_DISC_FUND_HV, AEGIS_IM_CTPY_COLUMNS, AEGIS_IM_ICE_COLUMNS,
    AEGIS_SIMM_CUTOFF_DATE
)
from src.config.paths import (
    AEGIS_IM_CTPY_FILE, AEGIS_IM_ICE_FILE,
    AEGIS_IM_CTPY_FUNDS_DIR_PATH, AEGIS_IM_ICE_FUNDS_DIR_PATH
)
from src.utils.data_io import load_excel_to_dataframe
from src.utils.formatter import str_to_date


def get_im_ctpy_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str ] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,
        
        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None
        
    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    filename = AEGIS_IM_CTPY_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_CTPY_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    dataframe, md5 = _read_im_all_history(date, fund, filename, paths_by_fund, schema_overrides, cutoff_date)

    return dataframe, md5


def get_im_ice_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str ] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,
        
        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None
        
    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    filename = AEGIS_IM_ICE_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_ICE_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    
    schema_overrides = AEGIS_IM_ICE_COLUMNS if schema_overrides is None else schema_overrides
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)
    
    dataframe, md5 = _read_im_all_history(date, fund, filename, paths_by_fund, schema_overrides, cutoff_date)
    
    return dataframe, md5


def get_im_ctpy_by_date (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        dataframe : Optional[pl.DataFrame] = None,
        md5 : Optional[str] = None,

    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    dataframe, md5 = get_im_ctpy_all_history(date, fund) if dataframe is None else (dataframe, md5)

    if dataframe is None :
        return None
    
    available_date = dataframe.filter(pl.col("Date") <= date).select(pl.col("Date").max()).item()

    if available_date is None :
        return _empty_simm_history_dataframe(AEGIS_IM_ICE_COLUMNS), None
    
    dataframe = dataframe.filter(pl.col("Date") == available_date)

    return dataframe, md5, available_date


def _read_im_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str ] = None,

        filename : Optional[str] = None,
        paths_by_fund : Optional[Dict] = None,
        
        schema_overrides : Optional[Dict] = None,
        cutoff_date : Optional[str | dt.datetime | dt.date] = None
        
    ) -> Tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    filename = AEGIS_IM_CTPY_FILE if filename is None else filename
    paths_by_fund = AEGIS_IM_CTPY_FUNDS_DIR_PATH if paths_by_fund is None else paths_by_fund
    
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    columns = list(schema_overrides.keys()) if schema_overrides is not None else None

    dir_abs_path = paths_by_fund.get(fund, None)
    
    if filename is None or dir_abs_path is None :
        return None, None
    
    file_abs_path = os.path.join(dir_abs_path, filename)
    print(file_abs_path)
    if not os.path.exists(file_abs_path) :
        return _empty_simm_history_dataframe(schema_overrides), None

    try :
        dataframe, md5 = load_excel_to_dataframe(file_abs_path, specific_cols=columns, schema_overrides=schema_overrides) 

    except Exception as e :

        log(f"Error during Excel lecture: {e}")
        return None, None
    
    cutoff_date = str_to_date(AEGIS_SIMM_CUTOFF_DATE if cutoff_date is None else cutoff_date)

    dataframe = dataframe.filter((pl.col("Date") >= (cutoff_date)) & (pl.col("Date") <= (date)))
    dataframe = dataframe.sort("Date")

    return dataframe, md5


def _empty_simm_history_dataframe (schema_overrides : Optional[Dict] = None) -> pl.DataFrame :
    """
    Build an empty SIMM history dataframe with the expected schema.
    """
    schema_overrides = AEGIS_IM_CTPY_COLUMNS if schema_overrides is None else schema_overrides
    dataframe = pl.DataFrame(schema=schema_overrides)

    return dataframe
