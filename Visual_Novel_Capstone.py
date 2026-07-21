import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json
import requests
from urllib.parse import quote
from gtts import gTTS


# =======================================================
# PAGE CONFIGURATION
# =======================================================

st.set_page_config(
    page_title="🎭 AI Visual Novel",
    page_icon="📖",
    layout="centered"
)


# =======================================================
# LOAD ENVIRONMENT VARIABLES
# =======================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API Key not found!")
    st.info(
        "Create a .env file and add:\n\n"
        "GEMINI_API_KEY=YOUR_API_KEY"
    )
    st.stop()


# =======================================================
# CACHE GEMINI CLIENT
# =======================================================

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=api_key)


client = get_gemini_client()


# =======================================================
# SESSION STATE - MEMORY VAULT
# =======================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "story_data" not in st.session_state:
    st.session_state.story_data = None


# =======================================================
# CUSTOM CSS
# =======================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef6ff, #ffffff);
}

h1 {
    text-align: center;
    color: #0B5394;
}

.story-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #f5f9ff;
    border: 1px solid #d9e8ff;
}

</style>
""", unsafe_allow_html=True)


# =======================================================
# HEADER
# =======================================================

st.title("🎭 AI Visual Novel")

st.write(
    "Create your own interactive adventure with "
    "AI-generated stories, visuals, choices, and narration."
)


# =======================================================
# SIDEBAR - STORY SETTINGS
# =======================================================

with st.sidebar:

    st.header("📖 Story Settings")

    story_genre = st.selectbox(
        "🎬 Story Genre",
        [
            "Fantasy",
            "Mystery",
            "Science Fiction",
            "Horror",
            "Adventure",
            "Romance"
        ]
    )

    art_style = st.selectbox(
        "🎨 Art Style",
        [
            "Photorealistic",
            "Anime",
            "Cinematic",
            "Digital Art",
            "Fantasy Art",
            "3D Render"
        ]
    )

    st.divider()

    if st.button(
        "🗑️ Restart Story",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.story_data = None

        st.rerun()


# =======================================================
# DISPLAY SETTINGS
# =======================================================

st.subheader("⚙️ Current Story Settings")

st.write(f"**Genre:** {story_genre}")
st.write(f"**Art Style:** {art_style}")


# =======================================================
# HELPER FUNCTION
# GENERATE STORY USING GEMINI
# =======================================================

def generate_story(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_response = response.text.strip()

    # Remove markdown code blocks if Gemini returns them
    if raw_response.startswith("```json"):

        raw_response = raw_response[7:]

        raw_response = raw_response.replace(
            "```",
            ""
        ).strip()

    elif raw_response.startswith("```"):

        raw_response = raw_response.replace(
            "```",
            ""
        ).strip()

    # Parse JSON
    story_data = json.loads(raw_response)

    return story_data


# =======================================================
# HELPER FUNCTION
# GENERATE IMAGE
# =======================================================

def generate_image(image_prompt, art_style):

    try:

        final_image_prompt = (
            f"{image_prompt}, "
            f"{art_style} style, "
            f"high quality, cinematic composition"
        )

        encoded_prompt = quote(
            final_image_prompt
        )

        image_url = (
            f"https://image.pollinations.ai/prompt/"
            f"{encoded_prompt}"
            f"?width=1024&height=768"
        )

        response = requests.get(
            image_url,
            timeout=30
        )

        if response.status_code == 200:

            return response.content

        else:

            st.toast(
                "Image server is busy, skipping visual..."
            )

            return None

    except Exception:

        st.toast(
            "Image server is busy, skipping visual..."
        )

        return None


# =======================================================
# HELPER FUNCTION
# GENERATE AUDIO
# =======================================================

def generate_audio(story_text):

    try:

        audio_file = "story_narration.mp3"

        tts = gTTS(
            text=story_text,
            lang="en"
        )

        tts.save(audio_file)

        return audio_file

    except Exception as e:

        st.warning(
            f"⚠️ Audio generation failed: {e}"
        )

        return None


# =======================================================
# DISPLAY STORY HISTORY
# =======================================================

st.divider()

st.subheader("📖 Story")

for message in st.session_state.messages:

    if message["role"] == "assistant":

        with st.chat_message("assistant"):

            st.markdown(
                message["content"]
            )

    elif message["role"] == "user":

        with st.chat_message("user"):

            st.markdown(
                message["content"]
            )


# =======================================================
# DISPLAY CURRENT IMAGE AND AUDIO
# =======================================================

if st.session_state.story_data:

    story_data = st.session_state.story_data

    image_prompt = story_data.get(
        "image_prompt",
        ""
    )

    story_text = story_data.get(
        "story_text",
        ""
    )


    # ---------------------------------------------------
    # GENERATE AND DISPLAY IMAGE
    # ---------------------------------------------------

    if image_prompt:

        with st.spinner(
            "🎨 Creating your visual scene..."
        ):

            image_data = generate_image(
                image_prompt,
                art_style
            )

        if image_data:

            st.image(
                image_data,
                caption=f"{art_style} Scene"
            )


    # ---------------------------------------------------
    # GENERATE AND DISPLAY AUDIO
    # ---------------------------------------------------

    if story_text:

        with st.spinner(
            "🔊 Creating story narration..."
        ):

            audio_file = generate_audio(
                story_text
            )

        if audio_file:

            st.audio(
                audio_file,
                format="audio/mp3"
            )


# =======================================================
# DYNAMIC CHOICE BUTTONS
# =======================================================

if st.session_state.story_data:

    options = st.session_state.story_data.get(
        "options",
        []
    )

    if options:

        st.divider()

        st.subheader(
            "🎮 What will you do?"
        )


        for index, option in enumerate(options):

            if st.button(
                option,
                key=f"option_{index}_{len(st.session_state.messages)}",
                use_container_width=True
            ):

                # ---------------------------------------
                # SAVE USER CHOICE
                # ---------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": option
                    }
                )


                # ---------------------------------------
                # BUILD CONVERSATION HISTORY
                # ---------------------------------------

                conversation = ""

                for message in st.session_state.messages:

                    conversation += (
                        f"{message['role']}: "
                        f"{message['content']}\n"
                    )


                # ---------------------------------------
                # GEMINI JSON PROMPT
                # ---------------------------------------

                prompt = f"""
You are the director of an interactive visual novel.

Story Genre:
{story_genre}

Art Style:
{art_style}

Conversation so far:
{conversation}

The player selected:
{option}

Continue the story based on the player's choice.

You MUST return ONLY a valid JSON object.

Do NOT use markdown.
Do NOT use ```json.
Do NOT add explanations outside the JSON.

The JSON must contain exactly these three keys:

{{
    "story_text": "A detailed narrative paragraph continuing the story.",

    "image_prompt": "A highly detailed prompt for an AI image generator describing the characters, environment, lighting, mood, camera angle, and visual style.",

    "options": [
        "First possible action",
        "Second possible action",
        "Third possible action"
    ]
}}

The options must contain 2 or 3 distinct choices.

Return ONLY valid JSON.
"""


                # ---------------------------------------
                # GENERATE NEXT STORY
                # ---------------------------------------

                with st.spinner(
                    "🌌 Creating the next chapter..."
                ):

                    try:

                        story_data = generate_story(
                            prompt
                        )


                        # -----------------------------------
                        # SAVE STORY
                        # -----------------------------------

                        story_text = story_data[
                            "story_text"
                        ]

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": story_text
                            }
                        )


                        # -----------------------------------
                        # SAVE STORY DATA
                        # -----------------------------------

                        st.session_state.story_data = (
                            story_data
                        )


                        st.rerun()


                    except json.JSONDecodeError:

                        st.error(
                            "❌ Gemini returned invalid JSON. "
                            "Please try again."
                        )


                    except Exception as e:

                        if "429" in str(e):

                            st.warning(
                                "⚠️ Gemini API quota exceeded. "
                                "Please try again later."
                            )

                        elif "503" in str(e):

                            st.warning(
                                "⚠️ Gemini is currently busy. "
                                "Please try again."
                            )

                        else:

                            st.error(
                                f"❌ Error: {e}"
                            )


# =======================================================
# START ADVENTURE
# =======================================================

if not st.session_state.messages:

    st.divider()

    st.info(
        "👋 Welcome, adventurer! "
        "Click below to begin your story."
    )


    if st.button(
        "🚀 Start Adventure",
        use_container_width=True
    ):

        prompt = f"""
You are the director of an interactive visual novel.

Story Genre:
{story_genre}

Art Style:
{art_style}

Create an exciting opening scene.

You MUST return ONLY a valid JSON object.

Do NOT use markdown.
Do NOT use ```json.
Do NOT add explanations outside the JSON.

The JSON must contain exactly these three keys:

{{
    "story_text": "An exciting opening narrative paragraph.",

    "image_prompt": "A highly detailed prompt for an AI image generator describing the characters, environment, lighting, mood, camera angle, and visual style.",

    "options": [
        "First possible action",
        "Second possible action",
        "Third possible action"
    ]
}}

The options must contain 2 or 3 distinct choices.

Return ONLY valid JSON.
"""


        with st.spinner(
            "🌌 Creating your adventure..."
        ):

            try:

                story_data = generate_story(
                    prompt
                )


                # ---------------------------------------
                # SAVE STORY
                # ---------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": story_data[
                            "story_text"
                        ]
                    }
                )


                # ---------------------------------------
                # SAVE STORY DATA
                # ---------------------------------------

                st.session_state.story_data = (
                    story_data
                )


                st.rerun()


            except json.JSONDecodeError:

                st.error(
                    "❌ Gemini returned invalid JSON."
                )


            except Exception as e:

                if "429" in str(e):

                    st.warning(
                        "⚠️ Gemini API quota exceeded. "
                        "Please try again later."
                    )

                elif "503" in str(e):

                    st.warning(
                        "⚠️ Gemini is currently busy. "
                        "Please try again."
                    )

                else:

                    st.error(
                        f"❌ Error: {e}"
                    )

