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

.stTextInput>div>div>input{
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
# Header (Requirement)
# -------------------------------------------------------
st.title("📡 The Identity Echo Interface")

st.write(
    "Welcome! Enter your **Name** and **Message**, then click **Transmit** to send your message through the Echo Interface."
)

st.divider()

# -------------------------------------------------------
# User Input Section
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

        st.success(
            f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}"
        )

        st.divider()

        with st.expander("📨 Transmission Details", expanded=True):

            st.write(f"**👤 Name:** {user_name}")
            st.write(f"**💬 Message:** {user_message}")

        characters = len(user_message)
        token_count = characters / 4

        st.info(
            f"🧠 System Check: Your message will consume approximately {token_count:.2f} tokens from our context window."
        )

        st.divider()

        st.subheader("📊 Message Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Characters",
                value=characters
            )

        with col2:
            st.metric("Estimated Tokens", f"{token_count:.2f}")

        st.progress(min(characters / 100, 1.0))

        st.info(
            f"🧠 System Check: Your message will consume approximately **{token_count:.2f} tokens** from our context window."
        )

        st.balloons()

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.divider()

st.markdown(
    "<div class='footer'>✨ Virtual Summer Internship 2026 | AI Builder Track | Streamlit Assignment</div>",
    unsafe_allow_html=True
)