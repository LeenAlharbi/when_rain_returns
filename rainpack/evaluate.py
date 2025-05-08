# rainpack/evaluate.py

import matplotlib.pyplot as plt
import seaborn as sns

def plot_temperature_trend(df):
    """
    Plot temperature over time for each city.
    """
    plt.figure(figsize=(14, 6))
    for city in df['City'].unique():
        city_df = df[df['City'] == city]
        plt.plot(city_df['DATE_ONLY'], city_df['AIR_TEMPERATURE'], label=city)
    
    plt.title('AIR_TEMPERATURE Over Time by City')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_precipitation_trend(df):
    """
    Plot precipitation over time for each city.
    """
    plt.figure(figsize=(14, 6))
    for city in df['City'].unique():
        city_df = df[df['City'] == city]
        plt.plot(city_df['DATE_ONLY'], city_df['precipitation_filled'], label=city)
    
    plt.title('Precipitation Over Time by City')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_heatmap_temperature(df):
    """
    Plot heatmap of average monthly temperatures for each city.
    """
    pivot_table = df.pivot_table(index='month', columns='City', values='AIR_TEMPERATURE', aggfunc='mean')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, cmap="coolwarm", fmt=".1f")
    plt.title('Average Monthly Temperature per City')
    plt.xlabel('City')
    plt.ylabel('Month')
    plt.show()
