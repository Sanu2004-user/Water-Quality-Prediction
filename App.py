import streamlit as st
import pandas as pd
import joblib

# Load model and column structure
model = joblib.load("pollution_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# Pollutants used in prediction
pollutants = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

# Pollution classification logic
def classify_pollution(pollutant, value):
    if pollutant == 'O2':
        if value < 5:
            return '❌ Very Low - Harmful'
        elif value < 8:
            return '⚠️ Medium - Caution'
        else:
            return '✅ Good - Safe'

    elif pollutant == 'NO3':
        if value > 10:
            return '❌ High - Harmful for drinking'
        elif value > 5:
            return '⚠️ Medium - Use caution'
        else:
            return '✅ Safe'

    elif pollutant == 'NO2':
        if value > 1:
            return '❌ High - Toxic'
        elif value > 0.2:
            return '⚠️ Medium - Monitor'
        else:
            return '✅ Safe'

    elif pollutant == 'SO4':
        if value > 250:
            return '❌ High - Not safe'
        elif value > 100:
            return '⚠️ Medium - Might affect taste'
        else:
            return '✅ Safe'

    elif pollutant == 'PO4':
        if value > 1:
            return '❌ High - Algae risk'
        elif value > 0.5:
            return '⚠️ Medium - Possible concern'
        else:
            return '✅ Safe'

    elif pollutant == 'CL':
        if value > 250:
            return '❌ High - Unsafe to drink'
        elif value > 100:
            return '⚠️ Medium - Might affect health'
        else:
            return '✅ Safe'

    return 'Unknown'

# Streamlit App UI
st.title("💧 Water Quality Prediction App")

# User input
station_id = st.selectbox("Select Station ID", [str(i) for i in range(1, 23)])
year_input = st.number_input("Enter the Year", min_value=2000, max_value=2030, value=2024)

# Predict button
if st.button("Predict Pollution Levels"):
    input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
    input_encoded = pd.get_dummies(input_df, columns=['id'])

    # Ensure all columns exist
    for col in model_columns:
        if col not in input_encoded:
            input_encoded[col] = 0

    input_encoded = input_encoded[model_columns]  # column order match

    # Predict
    prediction = model.predict(input_encoded)[0]

    st.subheader(f"🌊 Predicted pollutant levels for station {station_id} in {year_input}:")

    # Final verdict flag
    safe_flag = True

    for pollutant, value in zip(pollutants, prediction):
        status = classify_pollution(pollutant, value)
        st.write(f"**{pollutant}: {value:.2f} → {status}**")

        if "❌" in status:
            safe_flag = False

    # Final message
    st.markdown("---")
    if safe_flag:
        st.success("✅ Overall: Water is Safe for Use and Consumption")
    else:
        st.error("🚫 Warning: Water is Not Safe for Drinking")

