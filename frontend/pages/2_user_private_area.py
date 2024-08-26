"""Frontend: user private area."""  # noqa: INP001
import json

import requests
import streamlit as st

st.session_state.login = st.session_state.get("login")
my_username = st.session_state["login"]

# callbacks
def delete_user(my_username: str = my_username) -> None:
    """Delete user info."""
    api_endpoint = st.secrets["DEL_USER_ENDPOINT"]
    requests.delete(  # noqa: B018, S113
        url=api_endpoint,
        data=json.dumps(
            {
                "username": my_username,
                "email": "mail",
                "password": "pass",
            },
        ),
    ).text
    st.page_link("Hello.py", label="Go to main", use_container_width=True)


st.title(f"Hello, {my_username}")
st.empty()
col10, col11, col12, col13 = st.columns([5, 4, 5, 2], gap="small")
with col10:
    st.write(f"Username: {my_username}")
with col11:
    st.page_link("pages/1_change_user_info.py", label="Change user info")

with col12:
    del_button = st.button("Delete my profile")
    if del_button:
        with st.form("Are you sure?"):
            yes = st.checkbox("Yes, delete my account")
            submit_button = st.form_submit_button("Confirm", on_click=delete_user)
with col13:
    logout = st.button("logout")
    if logout:
        st.switch_page("Hello.py")

st.empty()


st.empty()
st.empty()
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

