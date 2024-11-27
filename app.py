import re
from yt_dlp import YoutubeDL
import streamlit as st

# Function to sanitize filenames
def sanitize_filename(filename):
    # Remove invalid characters for Windows filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Function to download YouTube videos
def download_video(url, resolution):
    try:
        # Extract video information without downloading
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = sanitize_filename(info_dict.get('title', 'video'))

        # Map resolutions to YouTube-DL format strings
        resolution_map = {
            "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
            "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]"
        }
        format_str = resolution_map.get(resolution, "best")

        # Set up the download options
        ydl_opts = {
            'format': format_str,
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

# Dropdown menu for resolution selection
resolution = st.selectbox(
    "Select resolution:",
    options=["360p", "480p", "720p"]
)

# Download button
if st.button("Download"):
    if url.strip():
        download_video(url, resolution)
    else:
        st.error("Please enter a valid YouTube URL.")
