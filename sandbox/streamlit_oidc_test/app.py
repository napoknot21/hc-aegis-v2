import streamlit as st

if not st.user.is_logged_in:
    st.login("microsoft")
else:
    st.write(f"Hello, {st.user.name}!")