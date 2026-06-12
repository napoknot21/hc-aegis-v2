import streamlit as st

if not st.user.is_logged_in :

    st.title("Aegis test")

    if st.button("Login with Microsoft"):
        st.login("microsoft")




else :


    st.write(f"Hello, {st.user.email}!")
    st.write(")")
    st.write(f"Hello, {st.user.name}!")

    if st.button("Logout"):
        st.logout()