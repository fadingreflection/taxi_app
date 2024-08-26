"""Frontend: user change info area."""  # noqa: INP001
import json

import requests
import streamlit as st

st.session_state.login = st.session_state.get("login")
my_username = st.session_state["login"]

# callbacks
def change_info(new_email: str, new_password: str) -> None:
    """Change user info."""
    api_endpoint = st.secrets["CHANGE_USER_INFO_ENDPOINT"]
    requests.patch(  # noqa: B018, S113
        url=api_endpoint,
        data=json.dumps(
            {
                "username": my_username,
                "email": new_email,
                "password": new_password,
            },
        ),
    ).text

st.header("UPDATE INFO FORM")

with st.form("Input your data here"):
    new_email = st.text_input("Type new email", key="new_mail")
    new_password = st.text_input("Type new password", key="new_passw")
    checkbox_val = st.checkbox(
        "I agree that the data provided is correct",
        )
    st.form_submit_button("Submit")
change_info(new_email, new_password)

st.page_link("pages/2_user_private_area.py", label="Update and return")
