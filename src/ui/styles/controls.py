from __future__ import annotations

import datetime as dt
from typing import Optional


subsections_controls_style = """
    <style>
    .section-title {
        background-color: #f5f5f5;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: 600;
        color: #333333;
        margin-top: 10px;
    }
    </style>
"""



def simm_colored_card (
    
        simm_value : float = 1.0,
        date : Optional[str | dt.datetime | dt.date] = None,
    
    ) -> str :
    """
    Returns color, label, and value for SIMM/NAV card-style display
    """
    if simm_value <= 18.0:
    
        color = "white"
        status = "🟢 Normal – No action required."
    
    elif simm_value <= 20.0:
    
        color = "rgba(255,165,0,0.3)"  # orange
        status = "🟠 Pre-breach zone – Escalation to AIFM Risk Officer."
    
    else:
        color = "rgba(255,0,0,0.3)"  # red
        status = "🔴 Breach – Immediate escalation."

    html = f"""
    <div style="background-color:{"white"};
                padding:16px;
                border:1px solid #ccc;
                border-radius:8px;
                text-align:center;
                font-weight:bold;
                font-family:Arial;
                margin-bottom:10px;">
        <div style="font-size:16px;">SIMM / NAV (%)</div>
        <div style="font-size:28px;">{simm_value:.2f} %</div>
    </div>
    """
    return html