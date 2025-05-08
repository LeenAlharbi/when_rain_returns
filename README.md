# ☁️ When Rain Returns: A Climate Forecast of Hope

This project forecasts the temperature and rainfall trends in Saudi Arabia's key cities (Riyadh and Jeddah) under two climate scenarios: baseline and improved (Saudi Green Initiative - SGI).

## 📂 Project Structure

- `main.py`: Run this script to generate temperature forecasts.
- `notebooks/`: Jupyter Notebooks with full exploration and modeling.
- `data/`: Cleaned datasets used in the models.
- `forecast_output.csv`: Sample forecast output.

## 🔧 Technologies

- Python, Pandas, Darts, Prophet, Matplotlib

## 📊 Models Used

- Prophet (for temperature forecasting)
- Croston, SBA, TSB (for sparse rainfall)
- Evaluation: MAPE, RMSE

## 🌱 Scenarios

- **Scenario A**: Forecast assuming no climate intervention
- **Scenario B**: Forecast with gradual temperature reduction (SGI impact)

## 📈 Results

Prophet models achieved validation MAPE under 10%, with seasonal breakdowns showing measurable improvement under the SGI scenario.

## 👥 Team Members

- **Leen Alharbi** — Project Lead & Data Scientist  
- **Fawzia Ibrahim** — Modeling & Experimentation & streamlit 
- **Dareen Alshaibani** — Modeling & Model Validation  
- **Aisha Alenzi** — FastAPI Integration & Support

## 🚀 How to Run

```bash
pip install -r requirements.txt
python main.py