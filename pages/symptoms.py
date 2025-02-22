import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

# Load API Key from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the LLM (Groq's Llama3-8B)
llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key=groq_api_key)

# Setup memory to retain chat history
memory = ConversationBufferMemory()

# Define prompt for patient symptom assessment
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template="""
    You are an AI-powered healthcare assistant.
    Your goal is to engage with patients and provide preliminary symptom assessment.
    You can ask follow-up questions to better understand their condition and suggest whether they should consult a doctor.
    
    Previous conversation:
    {history}
    
    Patient: {input}
    AI:
    """
)

# Create a conversational chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False,
    prompt=prompt_template
)

# Streamlit UI
st.title("🩺 AI Healthcare Assistant")
st.write("Chat with an AI-powered assistant for preliminary symptom assessment and guidance.")

# User input box
user_input = st.text_input("Describe your symptoms:", "")

if st.button("Get Report"):
    if user_input:
        response = conversation.predict(input=user_input)
        st.write(f"AI:{response}")
        
st.write("⚠️ Disclaimer: This AI is for informational purposes only and does not provide medical diagnoses. Please consult a doctor for professional medical advice.")