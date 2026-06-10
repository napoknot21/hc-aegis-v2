from __future__ import annotations

import datetime as dt
from typing import Any

import streamlit as st


st.set_page_config(
    page_title="Aegis Auth Test",
    page_icon="lock",
    layout="centered",
)


def get_user_value(key: str, default: Any = None) -> Any:
    """
    Safely read a claim from st.user.
    """
    try:
        return st.user.get(key, default)
    except Exception:
        return default


def render_login_screen() -> None:
    """
    Render a minimal login screen for the configured Microsoft provider.
    """
    st.title("Aegis Auth Test")
    st.write("Test rapide de `st.login()`, `st.logout()` et `st.user` avec Microsoft Entra ID.")
    st.info(
        "Genere d'abord la config Streamlit avec "
        "`python sandbox/streamlit_oidc_test/bootstrap_secrets.py`, "
        "ou renseigne manuellement `sandbox/streamlit_oidc_test/.streamlit/secrets.toml`."
    )

    if st.button("Login with Microsoft", type="primary"):
        st.login("microsoft")

    st.stop()


def render_identity_summary() -> None:
    """
    Render the main authenticated view.
    """
    name = get_user_value("name", "Unknown user")
    email = get_user_value("email") or get_user_value("preferred_username", "Unknown email")
    oid = get_user_value("oid", "N/A")
    tid = get_user_value("tid", "N/A")
    exp = get_user_value("exp")

    st.title("Aegis Auth Test")
    st.success("Authentication successful.")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Name**: {name}")
        st.write(f"**Email / Username**: {email}")
        st.write(f"**User Object ID**: `{oid}`")
        st.write(f"**Tenant ID**: `{tid}`")
        if exp is not None:
            expires_at = dt.datetime.fromtimestamp(int(exp), tz=dt.timezone.utc)
            st.write(f"**Token expiry (UTC)**: {expires_at.isoformat()}")

    with col2:
        if st.button("Logout", type="secondary", use_container_width=True):
            st.logout()

    with st.expander("Raw st.user payload", expanded=True):
        st.json(st.user.to_dict())

    with st.expander("Exposed tokens status", expanded=False):
        tokens = getattr(st.user, "tokens", {})
        token_info = {
            "id_token_exposed": bool(tokens.get("id")),
            "access_token_exposed": bool(tokens.get("access")),
        }
        st.json(token_info)
        st.caption(
            "Les tokens ne sont pas affiches ici pour eviter de les exposer dans l'UI. "
            "Si besoin, tu peux les utiliser cote serveur pour des appels API."
        )


def main() -> None:
    """
    Run the authentication test app.
    """
    is_logged_in = bool(getattr(st.user, "is_logged_in", False))

    if not is_logged_in:
        render_login_screen()

    render_identity_summary()


if __name__ == "__main__":
    main()
