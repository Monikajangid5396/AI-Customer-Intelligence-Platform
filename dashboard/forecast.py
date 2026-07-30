from prophet import Prophet
import pandas as pd

def sales_forecast(sales, periods=30):
    """
    Train Prophet model and forecast future sales.
    """

    # Daily revenue
    df = (
        sales.groupby("order_date")["total_amount"]
        .sum()
        .reset_index()
    )

    df.columns = ["ds", "y"]

    df["ds"] = pd.to_datetime(df["ds"])

    # Create model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    model.fit(df)

    # Future dates
    future = model.make_future_dataframe(periods=periods)

    forecast = model.predict(future)

    return model, forecast