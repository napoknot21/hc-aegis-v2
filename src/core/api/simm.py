from __future__ import annotations

import os
import polars as pl
import datetime as dt

from typing import Optional, Dict, Any, List


from src.utils import ice
from src.utils.ice import get_ice_calculator
from src.utils.date import today_previous_bussiness_day
from src.utils.formatter import str_to_date 

from src.config.parameters import AEGIS_DISC_FUND_HV

def fetch_simm_data (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        ic : Optional[Any] = None


    ) -> pl.DataFrame :
    """
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund
    
    ic = get_ice_calculator() if ic is not None else ic
    