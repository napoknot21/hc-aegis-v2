from __future__ import annotations

import os
import polars as pl

from dotenv import load_dotenv
from typing import Any, Optional

load_dotenv()


# ---------------------- MSAL (AEGIS Controls) ----------------------

AEGIS_MSAL_CLIENT_SECRET_VALUE = os.getenv("AEGIS_MSAL_CLIENT_SECRET_VALUE")
AEGIS_MSAL_CLIENT_SECRET_ID = os.getenv("AEGIS_MSAL_CLIENT_SECRET_ID")
AEGIS_MSAL_CLIENT_ID = os.getenv("AEGIS_MSAL_CLIENT_ID")
AEGIS_MSAL_TENANT_ID = os.getenv("AEGIS_MSAL_TENANT_ID")

AEGIS_MSAL_GRAPH_BASE = "https://graph.microsoft.com/v1.0"
AEGIS_MSAL_SCOPES = ["https://graph.microsoft.com/.default"]
AEGIS_MSAL_AUTHORITY = f"https://login.microsoftonline.com/{AEGIS_MSAL_TENANT_ID}"


AEGIS_MSAL_EMAIL_SENDER_MAIL = os.getenv("AEGIS_MSAL_EMAIL_SENDER_MAIL")
AEGIS_MSAL_EMAIL_RECIPIENT_MAIL = os.getenv("AEGIS_MSAL_EMAIL_RECIPIENT_MAIL")

AEGIS_MSAL_EMAIL_BREACH_LOG_SUBJECT = os.getenv("AEGIS_MSAL_EMAIL_BREACH_LOG_SUBJECT")
AEGIS_MSAL_EMAIL_BREACH_LOG_CONTENT = os.getenv("AEGIS_MSAL_EMAIL_BREACH_LOG_CONTENT")

AEGIS_MSAL_EMAIL_BREACH_COMM_SUBJECT = os.getenv("AEGIS_MSAL_EMAIL_BREACH_COMM_SUBJECT")
AEGIS_MSAL_EMAIL_BREACH_COMM_CONTENT = os.getenv("AEGIS_MSAL_EMAIL_BREACH_COMM_CONTENT")


# ---------------------- LOGGER (AEGIS Modules) ----------------------

AEGIS_LOGGER_NAME = "aegis"
AEGIS_LOGGER_LOGS_DIR_NAME = "logs"
AEGIS_LOGGER_FILE_PREFIX = "aegis"
AEGIS_LOGGER_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
AEGIS_LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"



# ---------------------- AEGIS UI - Controls ----------------------


# Disc Controls

AEGIS_DISC_CONTROLS_SUB_MENUS = [

    {"menu" : "Leverage", "icon" : "📐"},
    {"menu" : "VaR & SIMM", "icon" : "📈"},
    {"menu" : "Sensitivities", "icon" : "📊"},
    {"menu" : "P&L", "icon" : "📉"},
    {"menu" : "Counterparty", "icon" : "💼"},
    {"menu" : "Credit", "icon" : "💳"},
    {"menu" : "Operational", "icon" : "⚙️"},
    {"menu" : "ESG", "icon" : "🌱"},
    {"menu" : "Breach Validation", "icon" : "✔️"},
    {"menu" : "Risks Graphs and Stats", "icon" : "📊"}

]



# ---------------------- Aegis Funds ----------------------


AEGIS_DISC_FUND_HV = os.getenv("AEGIS_DISC_FUND_HV")
AEGIS_DISC_FUND_WR = os.getenv("AEGIS_DISC_FUND_WR")

AEGIS_DISC_FUNDS = {

    AEGIS_DISC_FUND_HV : "HV",
    AEGIS_DISC_FUND_WR : "WR"

}


# ---------------------- AEGIS Leverages ----------------------

AEGIS_LEVERAGES_ALL_SCHEMA_OVERRIDES = {

    "Gross Leverage" : pl.Float64,
    "Commitment Leverage" : pl.Float64,
    "Date" : pl.Datetime,
    #"File" : pl.Utf8

}


AEGIS_LEVERAGES_ALL_COLUMNS_SCHEMA_OVERRIDES = {

    "Gross Leverage" : pl.Float64,
    "Commitment Leverage" : pl.Float64,
    "Date" : pl.Datetime,
    "File" : pl.Utf8

}


# ---------------------- AEGIS SIMM / VaR ----------------------

AEGIS_IM_ICE_COLUMNS = {

    "Counterparty" : pl.Utf8,
    "IM" : pl.Float64,
    "MV" : pl.Float64,
    "MV Capped" : pl.Float64,
    "MV Capped Type" : pl.Float64,
    "Available / Shortfall Amount" : pl.Float64,
    "Client Margin Rate" : pl.Float64,
    "Date" : pl.Date

}

AEGIS_IM_CTPY_COLUMNS = {

    "Fundation" : pl.Utf8,
    "Account" : pl.Utf8,
    "Date": pl.Date,
    "Bank" : pl.Utf8,
    "Currency" : pl.Utf8,
    "Total" : pl.Float64,
    "IM" : pl.Float64,
    "VM" : pl.Float64,
    "Requirement" : pl.Float64,
    "Net Excess/Deficit" : pl.Float64

}

AEGIS_SIMM_CUTOFF_DATE = os.getenv("AEGIS_SIMM_CUTOFF_DATE")


# ---------------------- AEGIS Risks ---------------------- 

# L01 (Leverage Risk)

AEGIS_L01_RISK_LEVELS = [

    {
        "label" : "Normal",
        "from" : None,
        "to" : 275,
    },

    {
        "label" : "Alert",
        "from": 275,
        "to": 290,

    },

    {
        "label" : "Pre-Breach",
        "from": 290,
        "to": 300,

    },

    {
        "label" : "Breach",
        "from": 300,
        "to": None,

    },

]

AEGIS_L01_RISK_BACKGROUND_LEVELS = [

    {
        "label" : "Normal",
        "color": None,
        "opacity": None,
    },
    
    {
        "label" : "Alert",
        "color": "#2ca02c",
        "opacity": 0.14,
    },
    
    {
        "label" : "Pre-Breach",
        "color": "#f2c94c",
        "opacity": 0.18,
    },

    {
        "label" : "Breach",
        "color": "#8a0303",
        "opacity": 0.16,
    },

]

AEGIS_L01_RISK = {

    "levels" : AEGIS_L01_RISK_LEVELS,
    "background" : AEGIS_L01_RISK_BACKGROUND_LEVELS

}


# L02 (Leverage Risk)

AEGIS_L02_RISK_LEVELS = [

    {
        "label" : "Normal",
        "from" : -25,
        "to" : 25
    },

    {
        "label" : "Alert",
        "from": -30,
        "to": -25,

    },

    {
        "label" : "Alert",
        "from": 25,
        "to": 30,
    },

    {
        "label" : "Breach",
        "from" : None,
        "to" : -30
    },

    {
        "label" : "Breach",
        "from" : 30,
        "to" : None,
    },


]

AEGIS_L02_RISK_BACKGROUND_LEVELS = [

    {
        "label" : "Normal",
        "color": "#f2c94c",
        "opacity": 0.18,
    },

    {
        "label" : "Alert",
        "color": "#f2c94c",
        "opacity": 0.18,
    },

    {
        "label" : "Breach",
        "color": "#8a0303",
        "opacity": 0.16,
    }

]

AEGIS_L02_RISK = {

    "levels" : AEGIS_L02_RISK_LEVELS,
    "background" : AEGIS_L02_RISK_BACKGROUND_LEVELS

}


# L03 (Leverage Risk)

AEGIS_L03_RISK_LEVELS = [

    {
        "label" : "Normal",
        "from" : -25,
        "to" : 25
    },

    {
        "label" : "Alert",
        "from": -30,
        "to": -25,

    },

    {
        "label" : "Alert",
        "from": 25,
        "to": 30,
    },

    {
        "label" : "Breach",
        "from" : None,
        "to" : -30
    },

    {
        "label" : "Breach",
        "from" : 30,
        "to" : None,
    },


]

AEGIS_L03_RISK_BACKGROUND_LEVELS = [

    {
        "label" : "Normal",
        "color": "#f2c94c",
        "opacity": 0.18,
    },

    {
        "label" : "Alert",
        "color": "#f2c94c",
        "opacity": 0.18,
    },

    {
        "label" : "Breach",
        "color": "#8a0303",
        "opacity": 0.16,
    }


]

AEGIS_L03_RISK = {

    "levels" : AEGIS_L03_RISK_LEVELS,
    "background" : AEGIS_L03_RISK_BACKGROUND_LEVELS

}


AEGIS_RISKS = {

    "L01"  : AEGIS_L01_RISK,
    "L02"  : AEGIS_L02_RISK,
    "L03"  : AEGIS_L03_RISK,
    
    "S01"  : None,
    "S02"  : None,
    "S03"  : None,

    "D01"  : None,
    "GEQ"  : None,
    "GFX"  : None,
    "DS01" : None,
    "DGFX" : None,
    "V01"  : None,

    "PL01" : None,
    "PL02" : None,

    "LR01" : None,
    "CR01" : None,
    "CR03" : None,

}
