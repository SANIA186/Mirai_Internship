import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
from datetime import datetime

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="🌌 AI Multiverse",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------------------------------
# Load Gemini API
# -------------------------------------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API Key not found!")
    st.info("Create a .env file and add:\n\nGEMINI_API_KEY=YOUR_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

# -------------------------------------------------------
# Chat History
# -------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------------
# Custom CSS
# -------------------------------------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#eef6ff,#ffffff);
}

h1{
    text-align:center;
    color:#0B5394;
}

.stButton>button{
    width:100%;
    height:50px;
    border-radius:12px;
    background:#0F62FE;
    color:white;
    font-size:18px;
    font-weight:bold;
    border:none;
}

.stButton > button,
div[data-testid="stForm"] button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    background-color: #0F62FE !important;
    color: white !important;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover,
div[data-testid="stForm"] button:hover {
    background-color: #0043CE !important;
    color: white !important;
}

.chatbox{
    padding:12px;
    border-radius:10px;
    background:#F5F9FF;
    margin-bottom:10px;
    border-left:5px solid #0F62FE;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header
# -------------------------------------------------------
st.title("🌌 AI Multiverse")

st.write(
    "Enter **any character or profession**, ask your question, and let Gemini respond completely in that role."
)

st.divider()

# -------------------------------------------------------
# Input Form
# -------------------------------------------------------

with st.form("ai_form", clear_on_submit=True):

    st.subheader("🎮 Configure Your AI")

    character = st.text_input(
        "🎭 Act Like",
        placeholder="Example: Sherlock Holmes, Bollywood Director, Iron Man..."
    )

    st.caption(
        "💡 Examples: Sherlock Holmes • Iron Man • Data Science Mentor • Bollywood Director • Teacher"
    )

    mood = st.selectbox(
        "😊 AI Mood",
        [
            "Friendly",
            "Professional",
            "Funny",
            "Motivational",
            "Thoughtful",
            "Confident"
        ]
    )

    style = st.selectbox(
        "✍️ Response Style",
        [
            "Short",
            "Detailed",
            "Bullet Points",
            "Story",
            "Step-by-Step"
        ]
    )

    user_message = st.text_area(
        "💬 Your Question",
        placeholder="Type your question here..."
    )

    col1, col2 = st.columns(2)

    with col1:
        send = st.form_submit_button(
            "🚀 Send",
            use_container_width=True
        )

    with col2:
        clear = st.form_submit_button(
            "🗑 Clear Chat",
            use_container_width=True
        )

# -------------------------------------------------------
# Clear Chat
# -------------------------------------------------------
if clear:
    st.session_state.messages = []
    st.rerun()

# -------------------------------------------------------
# Generate Response
# -------------------------------------------------------
if send:

    if character.strip() == "":
        st.error("Please enter a character or profession.")

    elif user_message.strip() == "":
        st.warning("Please enter your question.")

    else:

        characters = len(user_message)
        token_count = characters / 4

        st.success("Prompt sent successfully!")

        st.info(
            f"🧠 Estimated Tokens: **{token_count:.2f}**"
        )

        prompt = f"""
You are {character}.

Stay completely in character.

AI Mood:
{mood}

Response Style:
{style}

Instructions:

• Never reveal that you are an AI.

• Behave exactly like {character}.

• Match the selected mood.

• Follow the selected response style.

• Be engaging and natural.

• If the user asks a technical question, explain it clearly.

User Question:

{user_message}
"""

        with st.spinner("🌌 Connecting to Gemini and entering the AI Multiverse..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                answer = response.text

                current_time = datetime.now().strftime("%I:%M %p")

                st.session_state.messages.append(
    {
        "character": character,
        "mood": mood,
        "style": style,
        "question": user_message,
        "answer": answer,
        "time": current_time
    }
)

            except Exception as e:
                st.error("Unable to connect to Gemini API.")
                st.exception(e)

# -------------------------------------------------------
# Chat History
# -------------------------------------------------------
# -------------------------------------------------------
# Chat History
# -------------------------------------------------------
if st.session_state.messages:

    st.divider()
    st.subheader("💬 Conversation")

    for chat in reversed(st.session_state.messages):

        with st.container(border=True):

            st.markdown(f"### 🎭 {chat['character']}")

            st.caption(
                f"😊 Mood: {chat['mood']} | ✍️ Style: {chat['style']} | 🕒 {chat['time']}"
            )

            st.markdown("#### 👤 Your Question")

            st.info(chat["question"])

            st.markdown("#### 🤖 AI Response")

            st.success(chat["answer"])

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.divider()

st.caption("✨ MirAI School of Technology | AI Multiverse | Powered by Gemini")