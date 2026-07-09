import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="The Identity Echo Interface",
    page_icon="📡",
    layout="centered"
)

# -------------------------------------------------------
# Load Gemini API Key
# -------------------------------------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API Key not found.")
    st.info("Create a .env file and add:\n\nGEMINI_API_KEY=YOUR_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

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

.stButton > button{
    width:100%;
    height:52px;
    border-radius:12px;
    background:#0F62FE;
    color:white;
    font-size:18px;
    font-weight:bold;
    border:none;
}

.stButton > button:hover{
    background:#0043CE;
    color:white;
}

.stTextInput > div > div > input{
    border-radius:10px;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header
# -------------------------------------------------------
st.title("📡 The Identity Echo Interface")

st.write(
    "Welcome! Enter your **Name** and **Message**, then click **Transmit** to send your message through the AI-powered Echo Interface."
)

st.divider()

# -------------------------------------------------------
# User Input
# -------------------------------------------------------
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

# -------------------------------------------------------
# Processing
# -------------------------------------------------------
if transmit:

    if user_name.strip() == "":
        st.error("Please provide your name.")

    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")

    else:

        # ---------------------------------------------
        # Assignment Requirement
        # ---------------------------------------------
        st.success(
            f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}"
        )

        # ---------------------------------------------
        # Transmission Details
        # ---------------------------------------------
        with st.expander("📨 Transmission Details", expanded=True):
            st.write(f"**👤 Name:** {user_name}")
            st.write(f"**💬 Message:** {user_message}")

        # ---------------------------------------------
        # Token Estimator (Optional Challenge)
        # ---------------------------------------------
        characters = len(user_message)
        token_count = characters / 4

        st.info(
            f"🧠 System Check: Your message will consume approximately **{token_count:.2f} tokens** from our context window."
        )

        st.subheader("📊 Message Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Characters", characters)

        with col2:
            st.metric("Estimated Tokens", f"{token_count:.2f}")

        st.progress(min(characters / 100, 1.0))

        # ---------------------------------------------
        # Gemini AI Response
        # ---------------------------------------------
        prompt = f"""
You are Echo AI.

The user's name is {user_name}.

The user sent this message:

"{user_message}"

Reply naturally.

Requirements:
- Greet the user by name.
- Be friendly and professional.
- Keep the response under 80 words.
"""

        with st.spinner("🤖 Connecting to Gemini..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.subheader("🤖 AI Echo Response")

                with st.container(border=True):
                    st.write(response.text)

                st.balloons()

            except Exception as e:

                st.error("Unable to connect to Gemini API.")
                st.exception(e)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.divider()

st.markdown(
    "<div class='footer'>✨ Virtual Summer Internship 2026 | AI Builder Track | Streamlit Assignment</div>",
    unsafe_allow_html=True
)