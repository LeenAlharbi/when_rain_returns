# rainpack/preprocessing.py

import pandas as pd

def add_time_features(df):
    """
    Add year and month features from DATE_ONLY.
    """
    df["year"] = df["DATE_ONLY"].dt.year
    df["month"] = df["DATE_ONLY"].dt.month
    return df

def detect_outliers(df, column):
    """
    Detect outliers using IQR method.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    upper_outliers = df[df[column] > upper_bound]
    lower_outliers = df[df[column] < lower_bound]
    return lower_outliers, upper_outliers
