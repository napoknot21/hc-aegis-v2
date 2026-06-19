from __future__ import annotations

from typing import Optional, Any, Dict, List

from src.config.parameters import AEGIS_RISKS


def build_risk_background_ranges (risk_config : Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]] :
    """
    Merge risk levels and background styles by label for chart shading.
    """
    risk_config = AEGIS_RISKS if risk_config is None else risk_config

    background_by_label = {
        
        background["label"] : background for background in risk_config.get("background", []) if background.get("label")
    
    }

    ranges = []

    for level in risk_config.get("levels", []) :

        background = background_by_label.get(level.get("label"))

        if not background or not background.get("color") :
            continue

        item = {

            "label" : level.get("label"),
            "from" : level.get("from"),
            "to" : level.get("to"),
            "color" : background.get("color"),
            
        }

        if background.get("opacity") is not None :
            item["opacity"] = background.get("opacity")

        ranges.append(item)

    return ranges