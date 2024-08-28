import pandas as pd
import sys
import os
sys.path.append(os.getcwd())

class Predictor:
    def __init__(
        self, model, job_type: str, input_date: str, input_distance: float | None
    ):
        self.model = model
        self.job_type = job_type
        self.input_date = input_date
        self.input_distance = input_distance

    def prepare_dataset(self):
        df = pd.DataFrame(
            columns=[
                "trip_distance",
                "hour",
                "weekday",
                "month",
            ],
            data=[
                [
                    self.input_distance,
                    self.input_date.hour,
                    self.input_date.weekday(),
                    self.input_date.month,
                ]
            ],
            index=[self.input_date],
        )
        df["is_holiday"] = df.weekday.apply(lambda x: 1 if x in [5, 6] else 0)
        df["is_friday"] = df.weekday.apply(lambda x: 1 if x == 4 else 0)
        return df

    def arima_pipeline(self, forecast_range):
        import warnings

        warnings.filterwarnings("ignore")
        from statsmodels.tsa.arima.model import ARIMA

        import plotly.graph_objects as go

        input_date = self.input_date

        df = pd.read_csv(
            "df_ts_rolled_resampled_15min.csv", index_col="tpep_pickup_datetime",
        )[["mean_bill"]]
        df.index = pd.to_datetime(df.index)
        y_test = df[df.index.date >= input_date.date()]
        y_train = y_test[y_test.index.date <= input_date.date() + pd.Timedelta("1d")]
        y_test = y_train[y_train.index >= input_date]
        y_test = y_test[
            y_test.index
            <= pd.to_datetime(input_date) + pd.Timedelta(f"{forecast_range}h")
        ]
        y_train = y_train[y_train.index < input_date]

        y_pred_wfv = pd.Series()
        history = y_train.copy()
        for i in range(len(y_test)):
            model = ARIMA(history, order=(7, 1, 1), freq="15min").fit()
            next_pred = model.forecast(freq="15min")
            next_pred.index = pd.to_datetime(next_pred.index)
            y_pred_wfv = pd.concat([y_pred_wfv, next_pred])
            history = pd.concat([history, y_test[y_test.index == next_pred.index[0]]])
            print(next_pred, end=" || ")

        # forecast plot
        fig = go.Figure()

        fig = fig.update_layout(
            title="New York taxi price forecast",
            xaxis_title="date, hour",
            yaxis_title="Average price per mile",
        )

        fig = fig.add_trace(
            go.Scatter(
                x=history[history.index <= input_date].index,
                y=history[history.index <= input_date]["mean_bill"],
                name="Actual price",
                line=dict(
                    color="green",
                    width=2,
                ),
            )
        )

        fig = fig.add_trace(
            go.Scatter(
                x=history[history.index >= input_date].index,
                y=history[history.index >= input_date]["mean_bill"],
                name="Forecast price",
                line=dict(
                    color="yellow",
                    width=2,
                    dash="dash",
                ),
            )
        )
        fig.update_traces(connectgaps=True)

        return fig

    def predict(self, df):
        result = self.model.predict(df)
        return result

    def predict_job(self, job_type: str, forecast_range: float | None = None):
        if job_type == "predict":
            df = self.prepare_dataset()
            result = self.predict(df)
            return format(result[0], ".2f")
        elif job_type == "forecast":
            result = self.arima_pipeline(forecast_range)
            return result