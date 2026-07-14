import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

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
# Session State
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

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header
# -------------------------------------------------------
st.title("🌌 AI Multiverse")

st.write(
    "Enter any character or profession, ask your question, and let Gemini respond in that role."
)

st.divider()

# -------------------------------------------------------
# AI Configuration
# -------------------------------------------------------
with st.sidebar:

    st.header("🎮 AI Configuration")

    character = st.text_input(
        "🎭 Act Like",
        placeholder="Sherlock Holmes, Teacher..."
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
    model_name = st.selectbox(
    "🤖 Gemini Model",
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro"
    ]
)
    st.divider()

    if st.button("🗑 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # -------------------------------------------------------
# Chat Input
# -------------------------------------------------------

if user_message := st.chat_input("Ask anything..."):

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Build conversation history
    conversation = ""

    for message in st.session_state.messages:
        conversation += f"{message['role']}: {message['content']}\n"

    # Build Prompt
    prompt = f"""
You are acting as {character}.

Mood:
{mood}

Response Style:
{style}

Rules:
- Stay completely in character.
- Never reveal that you are an AI.

Conversation so far:
{conversation}

Current User Question:
{user_message}
"""

    # Generate AI response
    with st.spinner("🌌 Entering the AI Multiverse..."):

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            answer = response.text
            st.success("✅ AI Response Generated")
            st.write(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()

        except Exception as e:
                error = str(e)

                if "429" in error:
                    st.warning("⚠️ Gemini API quota exceeded. Please wait a while and try again.")

                elif "503" in error:
                    st.warning("⚠️ Gemini is currently busy. Please try again in a few moments.")

                else:
                    st.error(f"Error: {e}")

    
    
# -------------------------------------------------------
# Conversation
# -------------------------------------------------------
st.divider()
st.subheader("💬 Conversation")


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


                # -------------------------------------------------------
# Download Conversation
# -------------------------------------------------------

chat_history = ""

if st.session_state.messages:

    for message in st.session_state.messages:

        role = "You" if message["role"] == "user" else character

        chat_history += f"{role}: {message['content']}\n\n"

else:

    chat_history = "No conversation yet."

with st.sidebar:

    st.divider()

    st.download_button(
        label="📥 Download Conversation",
        data=chat_history,
        file_name="AI_Multiverse_Chat.txt",
        mime="text/plain",
        use_container_width=True,
        key="download_chat"
    )