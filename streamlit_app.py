import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory

# Initialize the conversation chain with OpenAI and a memory buffer
api_key = st.secrets['openai_api_key']
chat = ChatOpenAI(temperature=0.7, openai_api_key = api_key, model_name='gpt-4o')  # You can replace this with any LLM provider

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | chat

chat_history = ChatMessageHistory()

# Streamlit app interface
st.title("Simple Chatbot with LangChain")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_input = st.text_input("You:", key="input")

if user_input:
    chat_history.add_user_message(user_input)
    st.session_state['messages'].append({"role": "user", "content": user_input})
    response = chain.invoke(
    {
        "messages": chat_history.messages,
    }
)
    chat_history.add_ai_message(response)
    st.session_state['messages'].append({"role": "assistant", "content": response})

for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.text_area("You:", message['content'], key=message['content'], height=100, disabled=True)
    else:
        st.text_area("Bot:", message['content'], key=message['content'], height=100, disabled=True)
