import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="The Identity Echo Interface",
    page_icon="📡",
    layout="centered"
)

# --------------------------------------------------
# Load API Key
# --------------------------------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------------------------------
# Custom Styling
# --------------------------------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(to bottom right,#EEF5FF,#FFFFFF);
}

h1{
    text-align:center;
    color:#0B5394;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:50px;
    font-size:18px;
    font-weight:bold;
    background:#0B5394;
    color:white;
}

.stButton>button:hover{
    background:#073763;
    color:white;
}

.stTextInput>div>div>input{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Assignment Requirement
# --------------------------------------------------
st.title("📡 The Identity Echo Interface")

st.write(
    "Enter your **Name** and **Message**, then click **Transmit** to send your message through the AI-powered Echo Interface."
)

st.divider()

# --------------------------------------------------
# User Input
# --------------------------------------------------
with st.container(border=True):

    st.subheader("🛰️ Transmission Console")

    user_name = st.text_input(
        "👤 Name",
        placeholder="Enter your name"
    )

    user_message = st.text_input(
        "💬 Message",
        placeholder="Type your message"
    )

    transmit = st.button("🚀 Transmit")

# --------------------------------------------------
# Processing
# --------------------------------------------------
if transmit:

    if user_name.strip() == "":
        st.error("Please provide your name.")

    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")

    else:

        # Assignment Requirement
        st.success(
            f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}"
        )

        # Token Estimator
        characters = len(user_message)
        token_count = characters / 4

        st.info(
            f"🧠 System Check: Your message will consume approximately {token_count:.2f} tokens from our context window."
        )

        st.divider()

        st.subheader("📊 Message Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Characters", characters)

        with col2:
            st.metric("Estimated Tokens", f"{token_count:.2f}")

        # Gemini Prompt
        prompt = f"""
You are Echo AI.

The user's name is {user_name}.

The user has sent this message:

"{user_message}"

Respond naturally.

• Greet the user by name.
• Be friendly.
• Keep the response under 80 words.
"""

        with st.spinner("🤖 Connecting to Gemini..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.divider()

                st.subheader("🤖 AI Echo Response")

                with st.container(border=True):
                    st.write(response.text)

                st.balloons()

            except Exception as e:

                st.error("Unable to connect to Gemini API.")
                st.exception(e)

st.divider()

st.caption("✨ MirAI School of Technology | AI Builder Track | Virtual Summer Internship 2026")