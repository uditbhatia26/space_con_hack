import streamlit as st

# Set page configuration
st.set_page_config(page_title="Health Assistant", page_icon="🏥", layout="centered")

# App title
st.title("🏥 Health Assistant")
st.write("Welcome to the Health Assistant app! Choose a service below.")

# Navigation links
st.sidebar.title("Navigation")
st.sidebar.page_link("pages/cheap_meds.py", label="💊 Cheap Medicines")
st.sidebar.page_link("pages/personalized_treatment.py", label="🩺 Personalized Treatment")
st.sidebar.page_link("pages/symptoms.py", label="🦠 Get your symptoms Checked")

st.header("🔹 Available Services")
st.page_link("pages/cheap_meds.py", label="💊 Find Cheap Medicine Alternatives")
st.page_link("pages/personalized_treatment.py", label="🩺 Get a Personalized Treatment Plan")
st.page_link("pages/symptoms.py", label="🦠 Get your symptoms Checked")

st.markdown("---")
st.info("⚠️ This app provides AI-generated recommendations. Always consult a doctor before making medical decisions.")
