import streamlit as st
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory

# Initialize the conversation chain with OpenAI and a memory buffer

#model https://huggingface.co/Orenguteng/Llama-3-8B-Lexi-Uncensored-GGUF

if 'chat' not in st.session_state:
    n_gpu_layers = 0  # Metal set to 1 is enough.
    n_batch = 128  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.

    st.session_state['chat'] = LlamaCpp(
        model_path=st.secrets['path_to_model'],
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=512,
        f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        verbose=True,
    )
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ChatMessageHistory()
if 'prompt' not in st.session_state:
    #st.session_state['prompt'] = ChatPromptTemplate.from_messages(
    #    [
    #        (
    #            "system",
    #            st.secrets['prompt'],
    #        ),
    #        MessagesPlaceholder(variable_name="chat_history"),
    #        ("human", "{input}"),
    #    ]
    #)
    st.session_state['prompt'] = PromptTemplate(
    template=st.secrets['prompt'],
    input_variables=["input"],
)

if 'chain' not in st.session_state:
    st.session_state['chain'] = st.session_state['prompt'] | st.session_state['chat']

if 'chain_with_message_history' not in st.session_state:
    st.session_state['chain_with_message_history'] = RunnableWithMessageHistory(
    st.session_state['chain'],
    lambda session_id: st.session_state['chat_history'],
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Streamlit app interface
st.title("Simple Chatbot with LangChain")

user_input = st.text_input("You:", key="input")

if user_input:
    #st.session_state['chat_history'].add_user_message(user_input)
    st.session_state['messages'].append({"role": "user", "content": user_input})
    #response = chain.invoke({"messages": st.session_state['chat_history'].messages,})
    #response = st.session_state['chain_with_message_history'].invoke({"input": user_input}, {"configurable": {"session_id": "unused"}},)
    response = st.session_state['chain'].invoke({"input": user_input})

    #st.session_state['chat_history'].add_ai_message(response.content)
    st.session_state['messages'].append({"role": "assistant", "content": response})

# Assuming that chat history is arranged in question-answer-question-answer...
for i in range(len(st.session_state['messages'])-1, -1, -2):
    message = st.session_state['messages'][i]
    if message['role'] == 'user':
        st.text_area("You:", message['content'], key=message['content'], height=100, disabled=True)
    else:
        st.text_area("Bot:", message['content'], key=message['content'], height=100, disabled=True)
