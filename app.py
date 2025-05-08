import streamlit as st
st.set_page_config(page_title="When Rain Returns", layout="wide")  # :white_check_mark: يجب أن يكون أول أمرimport plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import joblib# :art: خلفية الصفحة
bg_image_url = "https://i.postimg.cc/t4TN10Vj/Screenshot-1446-11-02-at-10-43-34-PM.png"
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)# :bricks: العنوان الرئيسي
st.title(":rain_cloud: When Rain Returns: Climate Forecast in Saudi Arabia")
st.markdown("""
Welcome to our interactive climate forecasting tool.
This app explores future temperature and rainfall under two scenarios:
- **Current Trends (No Intervention)**
- **With Saudi Green Initiative (SGI) Improvements**
""")# :page_facing_up: تحميل البيانات
df = pd.read_csv("all_cleand_dataset.csv")# :cityscape: اختيار المدينة والسنة
cities = df["City"].unique()
selected_city = st.selectbox("Select a City", cities)
selected_year = st.text_input("Select year", '2030')# :crystal_ball: دالة التنبؤ بالأمطار
def predict(start='2025', end='2030-12-31', City='Riyadh', df=None):
    clf = joblib.load(f'{City}_rain_classifier_model.joblib')
    reg = joblib.load(f'{City}_rain_regressor_model.joblib')    future_dates = pd.date_range(start=f'{start}-01-01', end=f'{end}', freq='D')
    future_df = pd.DataFrame({'date': future_dates})
    future_df['dayofyear'] = future_df['date'].dt.dayofyear
    future_df['month'] = future_df['date'].dt.month    last_known = df.iloc[-3:]['precipitation_filled'].values.tolist()
    predictions = []    for i in range(len(future_df)):
        row = future_df.iloc[i]
        input_features = {
            'dayofyear': row['dayofyear'],
            'month': row['month'],
            'lag1': last_known[-1],
            'lag2': last_known[-2],
            'lag3': last_known[-3],
        }
        X_input = pd.DataFrame([input_features])
        prob = clf.predict_proba(X_input)[:, 1][0]
        predicted_amt = reg.predict(X_input)[0]
        expected_rainfall = prob * predicted_amt
        predictions.append(expected_rainfall)
        last_known.append(expected_rainfall)
        last_known = last_known[-3:]    future_df['predicted_rainfall'] = predictions
    return future_df# :bar_chart: دالة رسم التنبؤات
def plot_predict(future_df):
    future_plot = future_df[['date', 'predicted_rainfall']].copy()
    future_plot.columns = ['date', 'rainfall']
    future_plot['type'] = 'forecast'    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(future_plot['date'], future_plot['rainfall'],
            label='Forecast', color='red', linestyle='--', alpha=0.9)
    ax.set_title("Rainfall: Forecast", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Rainfall (mm)")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    st.pyplot(fig)# :brain: تنفيذ التنبؤ عند الضغط
if st.button("Predict"):
    filtered = df[(df["City"] == selected_city)].sort_values(by='DATE_ONLY')
    if not filtered.empty:
        future_df = predict(end=selected_year, City=selected_city, df=filtered)
        plot_predict(future_df)
    else:
        st.warning("No data available for this selection.")temps_without_sgi = {
    2025: {"Riyadh": {"Spring": 27.5, "Summer": 43.2, "Autumn": 33.1, "Winter": 18.3},
           "Jeddah": {"Spring": 30.2, "Summer": 41.0, "Autumn": 35.0, "Winter": 23.4}},
    2026: {"Riyadh": {"Spring": 27.3, "Summer": 42.9, "Autumn": 32.9, "Winter": 18.0},
           "Jeddah": {"Spring": 30.1, "Summer": 40.8, "Autumn": 34.9, "Winter": 23.1}},
    2027: {"Riyadh": {"Spring": 27.1, "Summer": 42.6, "Autumn": 32.6, "Winter": 17.8},
           "Jeddah": {"Spring": 29.9, "Summer": 40.6, "Autumn": 34.7, "Winter": 22.9}},
    2028: {"Riyadh": {"Spring": 26.9, "Summer": 42.3, "Autumn": 32.3, "Winter": 17.5},
           "Jeddah": {"Spring": 29.8, "Summer": 40.4, "Autumn": 34.6, "Winter": 22.6}},
    2029: {"Riyadh": {"Spring": 26.6, "Summer": 42.0, "Autumn": 32.0, "Winter": 17.2},
           "Jeddah": {"Spring": 29.6, "Summer": 40.2, "Autumn": 34.4, "Winter": 22.3}},
    2030: {"Riyadh": {"Spring": 26.4, "Summer": 41.7, "Autumn": 31.7, "Winter": 17.0},
           "Jeddah": {"Spring": 29.5, "Summer": 40.0, "Autumn": 34.3, "Winter": 22.0}},
}
# بيانات درجات الحرارة مع SGI
temps_with_sgi = {
    2025: {"Riyadh": {"Spring": 26.8, "Summer": 42.5, "Autumn": 32.4, "Winter": 17.7},
           "Jeddah": {"Spring": 29.7, "Summer": 40.5, "Autumn": 34.5, "Winter": 22.8}},
    2026: {"Riyadh": {"Spring": 26.3, "Summer": 42.0, "Autumn": 32.0, "Winter": 17.2},
           "Jeddah": {"Spring": 29.4, "Summer": 40.0, "Autumn": 34.2, "Winter": 22.3}},
    2027: {"Riyadh": {"Spring": 25.8, "Summer": 41.5, "Autumn": 31.5, "Winter": 16.7},
           "Jeddah": {"Spring": 29.0, "Summer": 39.5, "Autumn": 33.8, "Winter": 21.9}},
    2028: {"Riyadh": {"Spring": 25.4, "Summer": 41.0, "Autumn": 31.1, "Winter": 16.3},
           "Jeddah": {"Spring": 28.6, "Summer": 39.0, "Autumn": 33.5, "Winter": 21.4}},
    2029: {"Riyadh": {"Spring": 24.9, "Summer": 40.5, "Autumn": 30.7, "Winter": 15.8},
           "Jeddah": {"Spring": 28.2, "Summer": 38.5, "Autumn": 33.1, "Winter": 21.0}},
    2030: {"Riyadh": {"Spring": 24.5, "Summer": 40.0, "Autumn": 30.3, "Winter": 15.4},
           "Jeddah": {"Spring": 27.8, "Summer": 38.0, "Autumn": 32.7, "Winter": 20.5}},
}
# واجهة المستخدم
st.title(":thermometer: Future Temperature Forecast (With & Without SGI)")
# اختيارات المستخدم
year = st.selectbox("Select Year", list(temps_without_sgi.keys()))
city = st.selectbox("Select City", ["Riyadh", "Jeddah"])
season = st.selectbox("Select Season", ["Spring", "Summer", "Autumn", "Winter"])
# استخراج القيم من القواميس
temp_without = temps_without_sgi[year][city][season]
temp_with = temps_with_sgi[year][city][season]
# عرض النتائج
st.subheader(f"Forecast for {city} - {season}, {year}")
st.metric("Without SGI", f"{temp_without:.1f} °C")
st.metric("With SGI", f"{temp_with:.1f} °C")