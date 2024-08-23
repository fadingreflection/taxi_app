import sys
import os
sys.path.append(os.getcwd())
from fastapi import APIRouter
from backend.predictor.predictor import Predictor
import pickle
import datetime
import json

loaded_model = pickle.load(open("backend\\model\\lreg_taxi.pkl", "rb"))

router=APIRouter()


@router.get("/ping")
def hello_page() -> str:
    return "This is taxi price prediction app main page"


@router.get("/predict_price")  # "%Y-%m-%d %H:%M:%S" for testing via swagger
def predict_price(input_date, input_dist) -> str:
    input_date = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    predictor_instance = Predictor(loaded_model, "predict", input_date, input_dist)
    result = predictor_instance.predict_job(
        job_type=predictor_instance.job_type, forecast_range=None
    )
    return f"The price of your taxi drive is {result} $"


@router.get("/get_forecast")
def get_forecast(input_date, input_dist, forecast_range):
    input_date = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    predictor_instance = Predictor(loaded_model, "forecast", input_date, input_dist)
    fig = predictor_instance.arima_pipeline(forecast_range=forecast_range)
    fig_dict = json.loads(fig.to_json())
    return fig_dict