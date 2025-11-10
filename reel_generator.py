import streamlit as st
import os
from moviepy.editor import *
from PIL import Image
import tempfile
from pathlib import Path

# Set page config
st.set_page_config(page_title="Facebook Reel Generator", layout="wide")

def create_text_clip(text, duration=3, fontsize=70, color='white', bg_color='transparent'):
    """Create a text clip with animation"""
    txt_clip = TextClip(text, fontsize=fontsize, color=color, bg_color=bg_color)
    txt_clip = txt_clip.set_position('center').set_duration(duration)
    # Add a fade in and fade out effect
    txt_clip = txt_clip.fadein(0.5).fadeout(0.5)
    return txt_clip

def create_image_clip(image_path, duration=3):
    """Create an image clip with zoom effect"""
    img_clip = ImageClip(image_path)
    # Resize to maintain aspect ratio but fill vertical space (reel format)
    w, h = img_clip.size
    target_h = 1920  # Instagram/Facebook reel height
    new_w = int(w * (target_h / h))
    img_clip = img_clip.resize(height=target_h)
    
    # If image is too wide, crop center
    if new_w > 1080:  # Instagram/Facebook reel width
        x_center = new_w // 2
        img_clip = img_clip.crop(x1=x_center-540, y1=0, x2=x_center+540, y2=target_h)
    
    # Add subtle zoom effect
    img_clip = img_clip.resize(lambda t: 1 + 0.05*t)
    img_clip = img_clip.set_position('center').set_duration(duration)
    
    return img_clip.fadein(0.5).fadeout(0.5)

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temp directory and return path"""
    if uploaded_file is not None:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

def main():
    st.title("📱 Facebook Reel Generator")
    st.write("Create engaging animated reels for Facebook with just a few clicks!")

    # Sidebar for template selection
    template = st.sidebar.selectbox(
        "Choose Template",
        ["Image Slideshow", "Quote with Background", "Text Animation"]
    )

    # Main content area
    if template == "Image Slideshow":
        st.subheader("🖼️ Image Slideshow")
        uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        transition_duration = st.slider("Transition Duration (seconds)", 1, 5, 3)
        
        if st.button("Generate Slideshow") and uploaded_files:
            try:
                with st.spinner("Creating your reel..."):
                    # Create clips for each image
                    clips = []
                    for uploaded_file in uploaded_files:
                        img_path = save_uploaded_file(uploaded_file)
                        if img_path:
                            clip = create_image_clip(img_path, transition_duration)
                            clips.append(clip)
                    
                    # Concatenate clips
                    final_clip = concatenate_videoclips(clips)
                    
                    # Save video
                    output_path = "output_reel.mp4"
                    final_clip.write_videofile(
                        output_path,
                        fps=30,
                        codec='libx264',
                        audio_codec='aac'
                    )
                    
                    # Show success and download button
                    st.success("✨ Your reel is ready!")
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Download Reel",
                            data=file,
                            file_name="facebook_reel.mp4",
                            mime="video/mp4"
                        )
                    
                    # Preview
                    st.video(output_path)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif template == "Quote with Background":
        st.subheader("💭 Quote with Background")
        quote_text = st.text_area("Enter Your Quote", height=100)
        background = st.file_uploader("Upload Background Image (Optional)", type=["jpg", "jpeg", "png"])
        duration = st.slider("Duration (seconds)", 3, 10, 5)
        
        if st.button("Generate Quote Reel") and quote_text:
            try:
                with st.spinner("Creating your quote reel..."):
                    # Create text clip
                    txt_clip = create_text_clip(quote_text, duration)
                    
                    if background:
                        # Use uploaded background
                        bg_path = save_uploaded_file(background)
                        bg_clip = create_image_clip(bg_path, duration)
                        final_clip = CompositeVideoClip([bg_clip, txt_clip])
                    else:
                        # Use black background
                        final_clip = txt_clip.on_color(
                            size=(1080, 1920),  # Instagram/Facebook reel size
                            color=(0, 0, 0),
                            duration=duration
                        )
                    
                    # Save video
                    output_path = "output_quote.mp4"
                    final_clip.write_videofile(
                        output_path,
                        fps=30,
                        codec='libx264',
                        audio_codec='aac'
                    )
                    
                    # Show success and download button
                    st.success("✨ Your quote reel is ready!")
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Download Reel",
                            data=file,
                            file_name="facebook_quote.mp4",
                            mime="video/mp4"
                        )
                    
                    # Preview
                    st.video(output_path)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    else:  # Text Animation
        st.subheader("✨ Text Animation")
        texts = st.text_area("Enter Text (one line per animation)", height=150)
        duration_per_text = st.slider("Duration per Text (seconds)", 1, 5, 2)
        
        if st.button("Generate Animation") and texts:
            try:
                with st.spinner("Creating your text animation..."):
                    # Split text into lines
                    text_clips = []
                    for text in texts.split('\n'):
                        if text.strip():
                            clip = create_text_clip(text.strip(), duration_per_text)
                            text_clips.append(clip)
                    
                    # Concatenate all text clips
                    final_clip = concatenate_videoclips(text_clips)
                    final_clip = final_clip.on_color(
                        size=(1080, 1920),  # Instagram/Facebook reel size
                        color=(0, 0, 0),
                        duration=final_clip.duration
                    )
                    
                    # Save video
                    output_path = "output_animation.mp4"
                    final_clip.write_videofile(
                        output_path,
                        fps=30,
                        codec='libx264',
                        audio_codec='aac'
                    )
                    
                    # Show success and download button
                    st.success("✨ Your animated reel is ready!")
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Download Reel",
                            data=file,
                            file_name="facebook_animation.mp4",
                            mime="video/mp4"
                        )
                    
                    # Preview
                    st.video(output_path)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Tips section
    with st.expander("💡 Tips for Great Reels"):
        st.markdown("""
        - Keep your videos between 15-60 seconds for optimal engagement
        - Use high-quality images (minimum 1080x1920 pixels)
        - Add background music to make your reels more engaging
        - Use contrasting colors for text to ensure readability
        - Keep text concise and easy to read
        - Test different templates to see what works best for your content
        """)

if __name__ == "__main__":
    main()