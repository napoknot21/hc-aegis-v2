from __future__ import annotations

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SECRETS_DIR = Path(__file__).resolve().parent / ".streamlit"
SECRETS_PATH = SECRETS_DIR / "secrets.toml"


def load_environment() -> None:
    """
    Load environment variables from the project root .env when present.
    """
    load_dotenv(PROJECT_ROOT / ".env")


def get_required_value(name: str) -> str:
    """
    Return a required environment variable when present.
    Fall back to an explicit placeholder for local test setup.
    """
    value = os.getenv(name)
    if value:
        return value

    placeholder_map = {
        "AEGIS_MSAL_CLIENT_ID": "replace-with-aegis-msal-client-id",
        "AEGIS_MSAL_CLIENT_SECRET_VALUE": "replace-with-aegis-msal-client-secret",
        "AEGIS_MSAL_TENANT_ID": "replace-with-aegis-tenant-id",
    }
    return placeholder_map[name]


def get_cookie_secret() -> str:
    """
    Reuse an existing cookie secret when present, otherwise generate one.
    """
    existing = os.getenv("AEGIS_STREAMLIT_COOKIE_SECRET")
    if existing:
        return existing

    return secrets.token_urlsafe(48)


def build_secrets_toml() -> str:
    """
    Build the Streamlit auth config from existing AEGIS MSAL variables.
    """
    client_id = get_required_value("AEGIS_MSAL_CLIENT_ID")
    client_secret = get_required_value("AEGIS_MSAL_CLIENT_SECRET_VALUE")
    tenant_id = get_required_value("AEGIS_MSAL_TENANT_ID")
    cookie_secret = get_cookie_secret()
    redirect_uri = os.getenv("AEGIS_STREAMLIT_REDIRECT_URI", "http://localhost:8501/oauth2callback")

    server_metadata_url = (
        f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
    )

    return (
        "[auth]\n"
        f'redirect_uri = "{redirect_uri}"\n'
        f'cookie_secret = "{cookie_secret}"\n'
        'expose_tokens = ["id", "access"]\n\n'
        "[auth.microsoft]\n"
        f'client_id = "{client_id}"\n'
        f'client_secret = "{client_secret}"\n'
        f'server_metadata_url = "{server_metadata_url}"\n'
    )


def main() -> int:
    """
    Generate the local Streamlit secrets file for the OIDC test app.
    """
    load_environment()
    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    SECRETS_PATH.write_text(build_secrets_toml(), encoding="utf-8")
    print(f"Wrote {SECRETS_PATH}")
    for env_name in (
        "AEGIS_MSAL_CLIENT_ID",
        "AEGIS_MSAL_CLIENT_SECRET_VALUE",
        "AEGIS_MSAL_TENANT_ID",
    ):
        if not os.getenv(env_name):
            print(f"Warning: {env_name} is missing, using a placeholder value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
