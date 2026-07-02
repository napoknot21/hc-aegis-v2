from __future__ import annotations

import os
import polars as pl
import datetime as dt

from typing import Optional, Dict, List, Any; tuple

from src.config.parameters import AEGIS_DISC_FUND_HV
from src.utils.formatter import str_to_date


def get_nav_history_all_history (
        
        date : Optional[str | dt.datetime | dt.date] = None,
        fund : Optional[str] = None,

        filename : Optional[str] = None,
        path_by_fund : Optional[Dict] = None,

        schema_overrides : Optional[Dict] = None,


    ) -> tuple[Optional[pl.DataFrame], Optional[str]] :
    """
    
    """
    date = str_to_date(date)
    fund = AEGIS_DISC_FUND_HV if fund is None else fund

    return None, None


