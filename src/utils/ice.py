from __future__ import annotations

import sys
import json
import polars as pl

from src.config.paths import LIBAPI_ABS_PATH
sys.path.append(LIBAPI_ABS_PATH)

from libapi.ice.trade_manager import TradeManager   # type: ignore
from libapi.ice.calcultor import IceCalculator      # type: ignore


def init_trade_manager () :
    """
    
    """
    return None