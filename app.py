import streamlit as st
import google.generativeai as genai
import time

# Configure Gemini AI
genai.configure(api_key="AIzaSyDY_kpM0SZWvWaP2gP22LayrUPhVdvPkNU")
model = genai.GenerativeModel("gemini-2.5-flash")

# Page configuration
st.set_page_config(
    page_title="SUNOBot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for chatbot UI with black and lavender colors
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f0f 0%, #2d1b69 100%);
        min-height: 100vh;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .chat-message {
        padding: 14px 18px;
        border-radius: 18px;
        margin-bottom: 16px;
        line-height: 1.5;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: fadeIn 0.3s ease-in;
    }
    .bot-message {
        background: linear-gradient(135deg, #6b46c1, #9f7aea);
        color: white;
        margin-right: auto;
        max-width: 75%;
        border-bottom-left-radius: 4px;
        border: none;
    }
    .user-message {
        background: linear-gradient(135deg, #2d3748, #4a5568);
        color: white;
        margin-left: auto;
        max-width: 75%;
        border-bottom-right-radius: 4px;
        border: none;
    }
    .bot-name {
        font-weight: bold;
        color: #d6bcfa;
        margin-bottom: 6px;
        font-size: 14px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-top: 2px solid rgba(159, 122, 234, 0.5);
        box-shadow: 0 -5px 20px rgba(0,0,0,0.3);
    }
    .input-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .chat-history {
        margin-bottom: 140px;
    }
    .header-section {
        background: linear-gradient(135deg, #2d1b69, #6b46c1);
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 10px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(107, 70, 193, 0.4);
        color: white;
    }
    .online-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #9f7aea;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    .stButton button {
        background: linear-gradient(135deg, #6b46c1, #9f7aea);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(107, 70, 193, 0.4);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(107, 70, 193, 0.6);
        background: linear-gradient(135deg, #5a3aa3, #805ad5);
    }
    .stTextInput input {
        border-radius: 25px;
        border: 2px solid #9f7aea;
        padding: 12px 20px;
        font-size: 14px;
        background: #1a202c;
        color: white;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #d6bcfa;
        box-shadow: 0 0 0 2px rgba(159, 122, 234, 0.3);
        background: #2d3748;
    }
    .stTextInput input::placeholder {
        color: #a0aec0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    .gradient-text {
        background: linear-gradient(135deg, #d6bcfa, #9f7aea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 2.5em;
    }
    .welcome-container {
        text-align: center;
        padding: 30px 20px;
        color: #a0aec0;
        background: rgba(26, 32, 44, 0.7);
        border-radius: 20px;
        margin: 10px 0;
        border: 1px solid rgba(159, 122, 234, 0.2);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .welcome-icon {
        font-size: 64px;
        margin-bottom: 15px;
        display: block;
    }
    .welcome-title {
        color: #9f7aea;
        margin-bottom: 10px;
        font-size: 24px;
        font-weight: bold;
    }
    .welcome-message {
        color: #cbd5e0;
        font-size: 16px;
        line-height: 1.6;
        max-width: 500px;
        margin: 0 auto;
    }
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1a202c;
    }
    ::-webkit-scrollbar-thumb {
        background: #6b46c1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #9f7aea;
    }
    /* Reduce spacing for the separator */
    .stMarkdown hr {
        margin: 5px 0;
        border: none;
        height: 1px;
        background: rgba(159, 122, 234, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header with black and lavender design
st.markdown("""
<div class="header-section">
    <div class="gradient-text">SUNOBot</div>
    <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">
        <span class="online-indicator"></span>
        <span style="font-size: 16px; font-weight: bold; color: #d6bcfa;">Online Now</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Chat container
with st.container():
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    
    # Display all messages
    for message in st.session_state.messages:
        if message["role"] == "bot":
            st.markdown(f'<div class="bot-name">SUNOBot</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        elif message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Welcome message if no messages yet
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="welcome-container">
            <div class="welcome-icon">🤖</div>
            <div class="welcome-title">Welcome to SUNOBot!</div>
            <div class="welcome-message">
                Hi friend! I'm your smart SUNOBot, here to make your day a little easier. What's on your mind?
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input area at bottom
st.markdown('<div class="input-area">', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

st.markdown("**💬 Reply to SUNOBot...**")

# Use form to prevent immediate rerun
with st.form(key="message_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Type your message:",
            placeholder="Type your message here... ✨",
            label_visibility="collapsed",
            key="user_input_field"
        )
    with col2:
        submit_button = st.form_submit_button("🚀 Send")

if submit_button and user_input.strip():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    
    # Generate bot response using Gemini AI
    with st.spinner("SUNOBot is thinking... ✨"):
        try:
            response = model.generate_content(user_input)
            bot_reply = response.text
        except Exception as e:
            bot_reply = "I apologize, but I'm having trouble processing your request right now. Please try again. 🔧"
        
        time.sleep(1)  # Simulate typing delay
        st.session_state.messages.append({"role": "bot", "content": bot_reply})
    
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)