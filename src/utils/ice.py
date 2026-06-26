from __future__ import annotations

import sys
import json
import polars as pl

from typing import Optional, List

from src.config.paths import LIBAPI_ABS_PATH
sys.path.append(LIBAPI_ABS_PATH)

from libapi.ice.trade_manager import TradeManager   # type: ignore
from libapi.ice.calculator import IceCalculator     # type: ignore

from src.utils.logger import log


def get_ice_calculator (loopback : int = 3) :
    """
    Initializes and returns a cached instance of IceCalculator.
    
    :param loopback: Number of retries connections
    :type loopback: int
    
    Returns:
        IceCalculator: An instance of the IceCalculator class used for ICE-related computations.
    """
    ice_calculator = None
    
    if loopback < 0 :

        log("[-] Connection failed to API Calculator after serveral retries.", "error")
        return ice_calculator

    try :
        
        ice_calculator = IceCalculator()
        log("[+] LibAPI successfully connected")

    except :

        print("[-] Error during LibAPI connection. Retrying...", "error")
        return get_ice_calculator(loopback - 1)

    return ice_calculator


#@st.cache_resource()
def get_trade_manager (loopback : int = 3) :
    """
    Initializes and returns a cached instance of TradeManager.

    Returns:
        TradeManager: An instance of the TradeManager class responsible for managing ICE trades.
    """
    trade_manager = None

    if loopback < 0 :

        log("[-] Connection failed to API for Trade Manager after serveral retries.", "error")
        return trade_manager
    
    try :

        trade_manager = TradeManager()
        log("[+] LibAPI successfully connected")

    except :

        print("[-] Error during LibAPI connection. Retrying...", "error")
        return get_trade_manager(loopback - 1)

    return trade_manager