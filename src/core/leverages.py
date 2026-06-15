from __future__ import annotations


import os
import polars as pl
import pandas as pd
import datetime as dt

from typing import Optional, Dict, List, Any

from src.config.parameters import AEGIS_DISC_FUNDS
from src.utils.formatter import str_to_date, date_to_str
from src.utils.data_io import load_excel_to_dataframe


def get_historical_leverage (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        paths_by_funds : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,
        dict_fund_name : Optional[Dict] = None,
        paths_by_fund : Optional[Dict] = None,

    ) :
    
    """
    
    """
    date = str_to_date(date)
    fund = "HV" if fund is None else fund

    dict_fund_name = AEGIS_DISC_FUNDS if dict_fund_name is None else dict_fund_name
    fund_fullname = dict_fund_name.get(fund, None)

    if fund_fullname is None :
        return None
    
    file_abs_path = 

    if not os.path.exists(file_abs_path) :

        return None
    


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