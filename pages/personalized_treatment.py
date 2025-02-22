import streamlit as st
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
import streamlit as st

st.set_page_config(page_title="Personalized Treatment Plan", page_icon="🩺")

st.title("🩺 Personalized Treatment Plan Generator")
st.write("Fill out the details below to get a tailored treatment plan based on your health data.")

# User Inputs
st.header("👤 Basic Information")
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
weight = st.number_input("Weight (kg)", min_value=10, max_value=300, step=1)
bmi = round(weight / ((height / 100) ** 2), 2) if height > 0 else "N/A"
st.write(f"Calculated BMI: **{bmi}**")

st.header("🏥 Medical History")
pre_existing_conditions = st.text_area("List any pre-existing conditions (e.g., Diabetes, Hypertension)")
current_symptoms = st.text_area("Describe your current symptoms")

st.header("💊 Current Medications & Lifestyle")
medications = st.text_area("List any ongoing medications (Name, Dosage, Frequency)")
smoking = st.radio("Do you smoke?", ["Yes", "No"])
alcohol = st.radio("Do you consume alcohol?", ["Yes", "No"])
sleep_hours = st.slider("Average sleep per night (hours)", 0, 12, 7)
stress_level = st.slider("Stress Level (1 - Low, 10 - High)", 1, 10, 5)

st.header("📑 Medical Test Reports (Optional)")
report = st.file_uploader(label="Upload your Medical Report (if any)")

st.header("⚕️ Treatment Preferences")
treatment_type = st.selectbox("Preferred treatment type", ["Allopathic", "Ayurvedic", "Homeopathic",     "No preference"])
budget = st.number_input("Budget for treatment (INR/USD)", min_value=0, step=100)

with open("sample_report.txt", "r", encoding="utf-8") as file:
    sample_data = file.read()

# Submit Button
if st.button("Generate Treatment Plan"):
    llm = ChatGroq(api_key=groq_api_key)
    st.success(f"Thank you, {name}! Your personalized treatment plan is being generated...")

    # Generate AI-based Treatment Plan (Replace with actual AI model call)
    prompt = f"""
    User Name: {name}
    Age of the User: {age}
    Gender: {gender}
    BMI of {name}: {bmi}
    List of any pre-existing conditions: {pre_existing_conditions}
    Current symptoms of the user: {current_symptoms}
    Does the user smoke: {smoking}
    Does the user consume alcohol: {alcohol} 
    Sleep hours of the user: {sleep_hours}
    Stress Level of the user on a scale of 1-10: {stress_level}
    Preferred Treatment type of the user: {treatment_type}
    Budget of the user: {budget}

    Based on the input provided by the user, you have to create a personalized, descriptive and accurate medical report for the user
    <sample>

    {sample_data}

    </sample>
    """
    report = llm.invoke(prompt)
    st.write(report.content)
    st.warning("⚠️ This is an AI-generated suggestion. Please consult a doctor before making any medical decisions.")

