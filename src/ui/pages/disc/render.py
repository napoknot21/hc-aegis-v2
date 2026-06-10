from __future__ import annotations

from typing import Optional, Dict

from src.ui.pages.disc.controls import controls
from src.ui.pages.disc.updater import updater


discretionary_subpages = [

    {"name" : "Controls",       "page" : controls,  "icon" : "cash-coin"},
    {"name" : "Updater",        "page" : updater,   "icon" : "eye"},

]



def render_disc (

        title : Optional[str] = "Discretionary Management",
        subtitle : Optional[str] = None,
        fundation_map : Optional[Dict] = None

    ) :
    """
    
    """


    return None