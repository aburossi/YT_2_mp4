import re
from yt_dlp import YoutubeDL
import streamlit as st

# Function to sanitize filenames
def sanitize_filename(filename):
    # Remove invalid characters for Windows filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Function to download YouTube videos
def download_video(url):
    try:
        # Extract video information without downloading
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = sanitize_filename(info_dict.get('title', 'video'))

        # Set up the download options
        ydl_opts = {
            'format': 'best[ext=mp4]',  # Best available MP4 format
            'quiet': True,
            'no_warnings': True,
            'outtmpl': f'{title}.mp4',  # Save video as the sanitized title
        }

        # Download the video to a temporary file
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Read the downloaded file and allow the user to download it via Streamlit
        with open(f"{title}.mp4", "rb") as file:
            st.download_button(
                label="Download video",
                data=file,
                file_name=f"{title}.mp4",
                mime="video/mp4"
            )
        st.success(f"Video '{title}' downloaded successfully!")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Streamlit app layout
st.title("YouTube Video Downloader")

# Input field for YouTube URL
url = st.text_input("Enter YouTube URL:")

# Download button
if st.button("Download"):
    if url.strip():
        download_video(url)
    else:
        st.error("Please enter a valid YouTube URL.")
