from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


# ----------------- MSAL (AEGIS Controls) ------------------

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


# ----------------- LOGGER (AEGIS Modules) ------------------

AEGIS_LOGGER_NAME = "aegis"
AEGIS_LOGGER_LOGS_DIR_NAME = "logs"
AEGIS_LOGGER_FILE_PREFIX = "aegis"
AEGIS_LOGGER_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
AEGIS_LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"



# ----------------- AEGIS UI - Controls ------------------

AEGIS_DISC_CONTROLS_SUB_MENUS = [

    {"menu" : "Leverage", "icon" : "📐"},
    {"menu" : "VaR & SIMM", "icon" : "📈"},
    {"menu" : "P&L", "icon" : "📉"},
    {"menu" : "Counterparty", "icon" : "💼"},
    {"menu" : "Credit", "icon" : "💳"},
    {"menu" : "Operational", "icon" : "⚙️"},
    {"menu" : "ESG", "icon" : "🌱"},
    {"menu" : "Breach Validation", "icon" : "✔️"},
    {"menu" : "Risks Graphs and Stats", "icon" : "📊"}

]



