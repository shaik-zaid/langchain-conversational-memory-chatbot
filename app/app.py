import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough


import warnings

warnings.filterwarnings("ignore")

# ─── Load environment variables ──────────────────────────────────────────────
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found. Please set it in your .env file")
    st.stop()

# ─── Initialize Groq model ──────────────────────────────────────────────────
# FIX 1: Changed from "openai/gpt-oss-120b" to "Gemma2-9b-It"
model = ChatGroq(
    model="openai/gpt-oss-120b",  
    groq_api_key=groq_api_key
)

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Memory-Enabled Conversational AI Chatbot")
st.caption("Remembers context, trims conversation history, and supports multiple languages.")

# ─── Sidebar configuration ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    
    language = st.selectbox(
        "Choose response language:",
        ["English", "Hindi", "Spanish", "French"]
    )
    
    max_tokens = st.slider(
        "Max tokens for history:",
        min_value=50,
        max_value=500,
        value=150,
        step=10,
        help="Lower values trim more messages to fit token limit"
    )
    
    enable_trimming = st.checkbox(
        "Enable message trimming",
        value=True,
        help="Automatically trim old messages to stay within token limit"
    )
    
    st.divider()
    
    if st.button("🗑️ Clear All Sessions"):
        st.session_state.store = {}
        st.session_state.messages = []
        st.rerun()

# ─── Session state initialization ──────────────────────────────────────────
if "store" not in st.session_state:
    st.session_state.store = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "main_chat"

# ─── Message history management ────────────────────────────────────────────
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create message history for a session"""
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

# ─── Setup prompt template with message placeholder ────────────────────────
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer in {language}. "
            "Use the conversation history to provide contextually relevant answers."
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)


# This ensures trimmer uses the current max_tokens value from slider
def create_chain(max_tokens_value, enable_trim):
    """Create chain with dynamic trimmer"""
    trimmer = trim_messages(
        max_tokens=max_tokens_value,
        strategy="last",
        token_counter=model,
        include_system=True,
        allow_partial=False,
        start_on="human"
    )
    
    if enable_trim:
        chain = (
            RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
            | prompt
            | model
        )
    else:
        chain = prompt | model
    
    return chain

# ─── Create chain with current settings ──────────────────────────────────────
chain = create_chain(max_tokens, enable_trimming)

# ─── Wrap chain with message history ───────────────────────────────────────────
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages"
)

# ─── Display conversation history ────────────────────────────────────────────
st.subheader("💬 Conversation")

# Get current session history
session_history = get_session_history(st.session_state.session_id)

# Display all messages
for msg in session_history.messages:
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ─── Chat input ────────────────────────────────────────────────────────────
if prompt_text := st.chat_input("Type your message..."):
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt_text)
    
    # Get response from model
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                config = {"configurable": {"session_id": st.session_state.session_id}}
                
                # Prepare input for the chain
                user_input = {
                    "messages": [HumanMessage(content=prompt_text)],
                    "language": language
                }
                
                # Get response from the chain
                response = with_message_history.invoke(
                    user_input,
                    config=config
                )
                
                response_text = response.content
                st.markdown(response_text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                response_text = f"Error occurred: {str(e)}"

# ─── Display statistics ────────────────────────────────────────────────────
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    session_history = get_session_history(st.session_state.session_id)
    msg_count = len(session_history.messages)
    st.metric("Messages", msg_count)

with col2:
    st.metric("Language", language)

with col3:
    trimming_status = "Enabled ✓" if enable_trimming else "Disabled ✗"
    st.metric("Trimming", trimming_status)

# ─── Show message history details ──────────────────────────────────────────
with st.expander("📜 View Full History"):
    session_history = get_session_history(st.session_state.session_id)
    if session_history.messages:
        for i, msg in enumerate(session_history.messages):
            role = "👤 User" if msg.type == "human" else "🤖 Assistant"
            st.write(f"**{role}** (Message {i+1})")
            st.write(msg.content)
            st.divider()
    else:
        st.info("No messages yet. Start a conversation!")

# ─── Show session management ──────────────────────────────────────────────
with st.expander("🔀 Manage Sessions"):
    st.write("Create or switch to different conversation sessions:")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        new_session = st.text_input("Session ID:", value=st.session_state.session_id)
    with col2:
        if st.button("Switch"):
            st.session_state.session_id = new_session if new_session else "main_chat"
            st.rerun()
    
    st.write("**Existing sessions:**")
    if st.session_state.store:
        for sid, hist in st.session_state.store.items():
            st.write(f"- `{sid}`: {len(hist.messages)} messages")
    else:
        st.info("No sessions yet")





