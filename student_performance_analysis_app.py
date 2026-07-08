import streamlit as st
import numpy as np
import joblib
from pathlib import Path

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

# -------------------------------------------------------
# Load Trained Model
# -------------------------------------------------------

MODEL_PATH = Path(__file__).parent / "best_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error("❌ best_model.pkl was not found.")
    st.info("Please place best_model.pkl in the same folder as this application.")
    st.stop()

# -------------------------------------------------------
# Title
# -------------------------------------------------------

st.title("🎓 Student Performance Predictor")

st.markdown(
"""
Predict a student's exam score using machine learning based on
their study habits and lifestyle.
"""
)

st.divider()

# -------------------------------------------------------
# User Inputs
# -------------------------------------------------------

study_hours = st.slider(
    "📚 Study Hours per Day",
    min_value=0.0,
    max_value=12.0,
    value=4.0,
    step=0.5
)

attendance = st.slider(
    "🏫 Attendance Percentage",
    min_value=0,
    max_value=100,
    value=80
)

mental_health = st.slider(
    "🧠 Mental Health Rating",
    min_value=1,
    max_value=10,
    value=5
)

sleep_hours = st.slider(
    "😴 Sleep Hours per Night",
    min_value=0.0,
    max_value=12.0,
    value=7.0,
    step=0.5
)

part_time_job = st.selectbox(
    "💼 Part-Time Job",
    ["No", "Yes"]
)

ptj = 1 if part_time_job == "Yes" else 0

st.divider()

# -------------------------------------------------------
# Prediction
# -------------------------------------------------------

if st.button("Predict Exam Score", use_container_width=True):

    input_data = np.array([[
        study_hours,
        attendance,
        mental_health,
        sleep_hours,
        ptj
    ]])

    try:
        prediction = model.predict(input_data)[0]

        prediction = float(np.clip(prediction, 0, 100))

        st.success(f"🎯 Predicted Exam Score: **{prediction:.2f}/100**")

        if prediction >= 90:
            st.balloons()
            st.info("🌟 Excellent Performance Expected!")

        elif prediction >= 75:
            st.info("✅ Very Good Performance Expected!")

        elif prediction >= 60:
            st.warning("🙂 Average Performance Expected.")

        else:
            st.error("⚠️ Student may need additional support.")

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.markdown("---")
st.caption("Student Performance Analysis Project | Machine Learning + Streamlit")