from __future__ import annotations

import streamlit as st

from src.auth.service import AuthService


def render_auth_page(auth_service: AuthService) -> None:
    st.title("LexiAssist")
    tab_login, tab_signup = st.tabs(["Login", "Sign up"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            try:
                user = auth_service.login(email=email.strip().lower(), password=password)
                st.session_state["user"] = user
                st.success("Logged in")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

    with tab_signup:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Create account"):
            try:
                auth_service.register(email=email.strip().lower(), password=password)
                st.success("Account created. Please log in.")
            except Exception as exc:
                st.error(str(exc))
