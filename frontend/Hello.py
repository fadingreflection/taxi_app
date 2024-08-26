"""Frontend entrypoint."""  # noqa: N999
import json
import os
import sys

import requests
import streamlit as st

sys.path.append(
    "C:\\Users\\Anastasiya Fedotova\\Desktop\\DS&ML\\github\taxi_app\\taxi_app",
)

#callbacks
def create_user(username, email, password) -> None:  # noqa: ANN001
    """Create new user."""
    api_endpoint = os.getenv("CREATE_USER_ENDPOINT")
    requests.post(  # noqa: B018, S113
        url=api_endpoint,
        data=json.dumps(
            {
                "username": username,
                "email": email,
                "password": password,
            },
        ),
    ).text

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

st.header("Register here")
with st.form("register_form"):
        username = st.text_input("username")
        email = st.text_input("email")
        password = st.text_input("password")
        submit = st.form_submit_button(
            "Register")

create_user(username,
            email,
            password,
            )

st.empty()
