from __future__ import annotations

import os
import polars as pl
import datetime as dt

from typing import Optional, Dict, Any, List; tuple


from src.utils.formatter import str_to_date
from src.utils.date import today_previous_bussiness_day 
from src.config.parameters import AEGIS_DISC_FUND_HV



