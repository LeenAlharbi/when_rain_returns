# rainpack/data_preparation.py

import pandas as pd
import numpy as np
from pathlib import Path
import glob

def load_and_merge_data(folder_path):
    """
    Load all CSV files from a folder and merge them into a single DataFrame.
    """
    data_dir = Path(folder_path)
    csv_files = glob.glob(str(data_dir / "*.csv"))
    
    dfs = []
    for f in csv_files:
        df = pd.read_csv(f, low_memory=False)
        df["source_file"] = Path(f).stem
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    return combined

def select_and_clean_columns(df):
    """
    Select important columns and fix temperature and precipitation values.
    """
    subset = df[["DATE", "NAME", "TEMP", "PRCP"]].copy()
    
    subset["TEMP"] = subset["TEMP"].replace([999.9, -9999], np.nan)
    subset["TEMP_C"] = (subset["TEMP"] - 32) * 5/9  # Convert to Celsius
    
    subset = subset[["DATE", "NAME", "TEMP_C", "PRCP"]]
    subset["DATE"] = pd.to_datetime(subset["DATE"], errors='coerce')
    subset.loc[(subset["TEMP_C"] < -50) | (subset["TEMP_C"] > 65), "TEMP_C"] = np.nan
    return subset

def fix_city_names(df):
    """
    Fix city names using a mapping.
    """
    mapping = {
        "HAIL, SA": "Hail",
        "KING KHALED INTERNATIONAL, SA": "Riyadh",
        "KING ABDULAZIZ INTERNATIONAL, SA": "Jeddah"
    }
    city_raw = df["City"].str.strip().str.upper()
    df["City"] = city_raw.replace(mapping).fillna(df["City"])
    return df

def final_rename_columns(df):
    """
    Rename columns to final names.
    """
    df = df.rename(columns={
        "TEMP_C": "AIR_TEMPERATURE",
        "PRCP": "precipitation_filled",
        "DATE": "DATE_ONLY"
    })
    return df
