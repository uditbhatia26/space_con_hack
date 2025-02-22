import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.tools import DuckDuckGoSearchRun
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Streamlit App Config
st.set_page_config(page_title="Affordable Medicine Finder", page_icon="💊")
st.title("💊 Affordable Medicine Finder")
st.write("Enter a medicine name or health condition, and I'll find cheaper alternatives for you!")

# Wikipedia and Web Search Tools
wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki_tool = Tool(name="Wikipedia Search", func=wiki_wrapper.run, description="Search Wikipedia for relevant information.")
search = DuckDuckGoSearchRun(name='Search')

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "Hello! Enter a medicine name or condition, and I'll find cheaper alternatives for you."}
    ]

# Display Chat History
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# User Input
if user_input := st.chat_input(placeholder="Enter a medicine name or health condition..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # LLM with Custom Prompt
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=groq_api_key)
    prompt_template = PromptTemplate(
        template="""
        You are a healthcare assistant specializing in finding affordable medicine alternatives.
        Given a medicine name or health condition, search for generic and cost-effective alternatives available in the market.
        Provide reliable information from trustworthy sources. Ensure the recommendations are relevant and accessible.
        
        Medicine/Condition: {query}
        """,
        input_variables=["query"]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    # Define Agent
    tools = [search, wiki_tool]
    medicine_agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors=True)

    # Get Response
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        response = medicine_agent.run(user_input, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
