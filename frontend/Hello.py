"""Frontend entrypoint."""  # noqa: N999
import json
import os
import sys

import requests
import streamlit as st

sys.path.append(
    "C:\\Users\\Anastasiya Fedotova\\Desktop\\DS&ML\\github\taxi_app\\taxi_app",
)


def create_user(username: str, email: str, password: str) -> None:
    """Create new user."""
    api_endpoint = os.getenv("CREATE_USER_ENDPOINT")
    response = requests.post(  # noqa: S113
        url=api_endpoint,
        data=json.dumps(
            {
                "username": username,
                "email": email,
                "password": password,
            },
        ),
    ).text
    st.write(response)


st.title("WELCOME to NEW YORK TAXI APP")

col1, col2 = st.columns(2)
with col1:
    login = st.text_input("login", key="login")
with col2:
    password = st.text_input("password", key="password")

st.empty()

col3, col4, col5 = st.columns([4, 5, 4])
with col4:
    login_button = st.button("login", use_container_width=True)
if login_button:
    api_endpoint = st.secrets["LOGIN_ENDPOINT"]
    response = requests.get(  # noqa: S113
        url=api_endpoint,
        params={
            "username": login,
            "password": password,
        },
    ).text
    if "token" in response:
        st.switch_page("pages/2_user_private_area.py")
    else:
        st.write("Incorrect login or password")

with st.form("Register form"):
    st.session_state["username"] = st.text_input("username")
    st.session_state["email"] = st.text_input("email")
    password = st.text_input("password")
    submit = st.form_submit_button(
        "Register",
        on_click=create_user(
            st.session_state["username"], st.session_state["email"], password,
        ),
    )


st.empty()
