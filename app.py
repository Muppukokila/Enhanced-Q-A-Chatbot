from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Now you can access your API key from the environment
api_key = os.getenv("LANGCHAIN_API_KEY")


load_dotenv()

# Langsmith Tracking
api_key = os.getenv("LANGCHAIN_API_KEY",
                    "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")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A Chatbot With Ollama"

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful massistant . Please  repsonse to the user queries"),
        ("user", "Question:{question}")
    ]
)


def generate_response(question, llm, temperature, max_tokens):
    llm = Ollama(model=llm)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer


# Title of the app
st.title("Enhanced Q&A Chatbot With OpenAI")


# Select the OpenAI model
llm = st.sidebar.selectbox("Select Open Source model", ["gemma:2b"])

# Adjust response parameter
temperature = st.sidebar.slider(
    "Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider(
    "Max Tokens", min_value=50, max_value=300, value=150)

# MAin interface for user input
st.write("Goe ahead and ask any question")
user_input = st.text_input("You:")


if user_input:
    response = generate_response(
        user_input, llm, temperature, max_tokens)  # Lower the max_tokens

    st.write(response)
else:
    st.write("Please provide the user input")
