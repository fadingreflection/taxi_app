"""Predictor endpoints."""
import datetime
import json
import pickle

from fastapi import APIRouter

from predictor.predictor import Predictor

loaded_model = pickle.load(open("lreg_taxi.pkl", "rb"))  # noqa: PTH123, S301, SIM115
router=APIRouter()


@router.get("/ping")
def hello_page() -> str:
    """Hello func."""
    return "This is taxi price prediction app main page"


@router.get("/predict_price")  # "%Y-%m-%d %H:%M:%S" for testing via swagger
def predict_price(input_date, input_dist) -> str:  # noqa: ANN001
    """Predict price."""
    input_date = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
    predictor_instance = Predictor(loaded_model, "predict", input_date, input_dist)
    result = predictor_instance.predict_job(
        job_type=predictor_instance.job_type, forecast_range=None,
    )
    return f"The price of your taxi drive is {result} $"


@router.get("/get_forecast")
def get_forecast(input_date, input_dist, forecast_range):  # noqa: ANN001, ANN201
    """Get forecast."""
    input_date = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
    predictor_instance = Predictor(loaded_model, "forecast", input_date, input_dist)
    fig = predictor_instance.arima_pipeline(forecast_range=forecast_range)
    return json.loads(fig.to_json())
