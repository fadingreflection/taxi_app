"""Frontend: user private area."""  # noqa: INP001
import json

import requests
import streamlit as st

my_username = "Anastasiya Fedotova"


# callback
def change_info(new_email: str, new_password: str) -> None:
    """Change user info."""
    api_endpoint = st.secrets["CHANGE_USER_INFO_ENDPOINT"]
    response = requests.patch(  # noqa: S113
        url=api_endpoint,
        data=json.dumps(
            {
                "username": my_username,
                "email": new_email,
                "password": new_password,
            },
        ),
    ).text
    st.write(new_email)
    st.write(response)
    st.write("Information updated.")


def delete_user() -> None:
    """Delete user info."""
    api_endpoint = st.secrets["DEL_USER_ENDPOINT"]
    response = requests.delete(  # noqa: S113
        url=api_endpoint,
        data=json.dumps(
            {
                "username": my_username,
                "email": "mail",
                "password": "pass",
            },
        ),
    ).text
    st.write(response)
    st.page_link("Hello.py", label="Go to main")


st.title(f"Hello, {my_username}")
st.empty()
st.empty()
col10, col11, col12 = st.columns([5, 4, 2], gap="large")
with col10:
    st.write(f"Username: {my_username}")
    st.write(f"email: {None}")
with col11:
    change_button = st.button("Change user info")
if change_button:
    with st.form("Input your data here"):
        new_email = st.text_input("Type new email")
        st.write(new_email)
        new_password = st.text_input("Type new password")
        checkbox_val = st.checkbox(
            "I agree that the data provided is correct",
        )
        st.write(new_email)
        submit_button = st.form_submit_button(
            "Submit", on_click=change_info(new_email, new_password),
        )
with col12:
    logout = st.button("logout")
    if logout:
        st.switch_page("Hello.py")

st.empty()


st.empty()
st.empty()
del_button = st.button("Delete my profile")
if del_button:
    with st.form("Are you sure?"):
        yes = st.checkbox("Yes, delete my account")
        submit_button = st.form_submit_button("Confirm", on_click=delete_user)


st.empty()
st.subheader("My trip history")
api_endpoint = st.secrets["GET_USER_TRIPS_ENDPOINT"]
response = requests.get(  # noqa: S113
    url=api_endpoint,
    params={
        "username": my_username,
    },
).text
response = json.loads(
    response,
)  # convert string to normal json structure --> then its possible to make table
st.table(response)

st.subheader("Calculate my trip")
_button = st.page_link("pages/3_taxi_app.py", label="Go to trip price calculator")
st.empty()
