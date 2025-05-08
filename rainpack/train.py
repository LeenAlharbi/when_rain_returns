# rainpack/train.py

from prophet import Prophet

def train_prophet(df, prediction_years=6):
    """
    Train a Prophet model on the provided dataframe and forecast until 2030.
    
    Args:
    - df: DataFrame with at least 'DATE_ONLY' and 'precipitation_filled' columns.
    - prediction_years: Number of years to forecast into the future (default 6 years from 2024 to 2030).
    
    Returns:
    - model: Trained Prophet model.
    - forecast: Forecasted values DataFrame.
    """
    # Step 1: تجهيز البيانات
    df_prophet = df.rename(columns={'DATE_ONLY': 'ds', 'precipitation_filled': 'y'})[['ds', 'y']]
    
    # تأكد من عدم وجود NaN
    df_prophet = df_prophet.dropna()
    
    # Step 2: بناء الموديل
    model = Prophet()
    model.fit(df_prophet)
    
    # Step 3: إنشاء DataFrame المستقبل للتوقع
    future = model.make_future_dataframe(periods=prediction_years * 365, freq='D')
    
    # Step 4: التوقع
    forecast = model.predict(future)
    
    return model, forecast

def plot_forecast(model, forecast, start_date=None, end_date=None):
    """
    Plot the forecasted precipitation with confidence intervals.
    
    Args:
    - model: Trained Prophet model.
    - forecast: Forecast DataFrame returned by Prophet.
    - start_date: Optional, to zoom into a specific start date.
    - end_date: Optional, to zoom into a specific end date.
    """
    import matplotlib.pyplot as plt
    
    if start_date and end_date:
        forecast_filtered = forecast[(forecast['ds'] >= start_date) & (forecast['ds'] <= end_date)]
    else:
        forecast_filtered = forecast

    plt.figure(figsize=(14, 6))
    plt.plot(forecast_filtered['ds'], forecast_filtered['yhat'], label='Predicted Precipitation', color='black')
    plt.fill_between(forecast_filtered['ds'], forecast_filtered['yhat_lower'], forecast_filtered['yhat_upper'], color='blue', alpha=0.2, label='Confidence Interval')
    plt.title('Forecasted Precipitation')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
