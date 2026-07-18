import streamlit as st
import requests
import random
from urllib.parse import quote

st.title("🎨 AI Image Studio")

st.sidebar.header("SETTINGS")
art_style=st.sidebar.selectbox(
    "Select desired Art Style",
    ["Photorealistic","Anime","Vintage Victorian","Sketch","3D Render"]
)

width=st.sidebar.slider("Image width",min_value=256,max_value=1024,value=768)
height=st.sidebar.slider("Image height",min_value=256,max_value=1024,value=768)
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

user_prompt=st.text_input("Decribe the image you want to generate")
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon drinking tea in a magical library",
    "A futuristic city floating above clouds",
    "A robot painting the Mona Lisa"
]

generate = st.button("Generate Image")

surprise = st.button("🎲 Surprise Me!")

if surprise:
    user_prompt = random.choice(surprise_prompts)


if generate or surprise:

    if user_prompt:

        with st.spinner("Rendering the image"):

            full_prompt = f"{user_prompt}, make the art style: {art_style}"


            # Magic Enhance Feature
            if magic_enhance:
                full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"


            # Width and Height Fix
            encoded_prompt = quote(full_prompt)

            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"

            response = requests.get(url)


            if response.status_code == 200:

                st.success("Image Generated")

                st.image(
                    response.content,
                    caption=full_prompt
                )


                # Download Image
                st.download_button(
                    label="📥 Download Image",
                    data=response.content,
                    file_name=f"{art_style}_image.png",
                    mime="image/png"
                )
                st.success("Image ready for download!")


            else:
               
                    st.error(f"API Error: {response.status_code}")
                    st.write(response.text)