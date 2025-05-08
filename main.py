import pandas as pd
import numpy as np
from darts import TimeSeries
from darts.models import Prophet
import os

# ========== setting ==========
CITY_NAME = "Riyadh"  
INPUT_PATH = "raw_data/all_cleand_dataset.csv"
OUTPUT_PATH = f"output/forecast_{CITY_NAME.lower()}.csv"

# ========== load data ==========
print(f"Loading data for {CITY_NAME}...")
df = pd.read_csv(INPUT_PATH, parse_dates=["DATE_ONLY"])
df_city = df[df["City"] == CITY_NAME].groupby("DATE_ONLY").mean().reset_index()

# ========== trans form to TimeSeries ==========
ts = TimeSeries.from_dataframe(
    df_city,
    time_col="DATE_ONLY",
    value_cols="AIR_TEMPERATURE",
    fill_missing_dates=True,
    freq="D"
)

# ========== prepare and train ==========
print("Training Prophet model...")
ts_train = ts.slice(pd.Timestamp("2005-01-01"), pd.Timestamp("2024-12-31"))
model = Prophet()
model.fit(ts_train)

# ========== prediction for 6 years ==========
print("Forecasting 2025–2030...")
forecast = model.predict(n=6 * 365)

# ========== save results ==========
forecast_df = pd.DataFrame({
    "Date": forecast.time_index,
    "Predicted_Temperature": forecast.values().flatten()
})

os.makedirs("output", exist_ok=True)
forecast_df.to_csv(OUTPUT_PATH, index=False)
print(f"Forecast saved to {OUTPUT_PATH}")
