import streamlit as st
import plotly.graph_objects as go
import requests
import plotly.io

st.title("NYC taxi price calculator :taxi: ")
st.image("taxi_logo.png", width=120)

col1, col2, col3 = st.columns(3)
with col1:
    my_date = st.date_input("Input date here")
with col2:
    my_time = st.time_input("Input time here", step=300)
with col3:
    my_dist = st.number_input("Input distance here", min_value=0.1)

st.empty()


dt_string = f"{my_date} {my_time}"

# PREDICT JOB
if "predicted_price" not in st.session_state:
    st.session_state.predicted_price = 0.0

prediction_button = st.button("Calculate")
if prediction_button:
    api_endpoint = st.secrets["PREDICT_ENDPOINT"]
    st.session_state.predicted_price = requests.get(
        url=api_endpoint, params={"input_date": dt_string, "input_dist": my_dist}
    ).text
st.write(st.session_state.predicted_price)

st.empty()

# FORECAST JOB
if "fig_forecast" not in st.session_state:
    st.session_state.fig_forecast = go.Figure()
    st.session_state.forecast_range = 0.0

forecast_range = st.number_input("input forecast range here")
st.empty()
st.empty()
forecast_button = st.button(f"Get price forecast for {forecast_range} hours")


if forecast_button:
    st.session_state.forecast_range = forecast_range
    api_endpoint = st.secrets["FORECAST_ENDPOINT"]
    json_string = requests.get(
        url=api_endpoint,
        params={
            "input_date": dt_string,
            "input_dist": my_dist,
            "forecast_range": st.session_state.forecast_range,
        },
    ).text
    fig = plotly.io.from_json(json_string)
    st.session_state.fig_forecast = fig

st.plotly_chart(st.session_state.fig_forecast)