import streamlit as st
from pytube import YouTube
import os
import re

# Function to validate YouTube URL
def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    return youtube_regex.match(url) is not None

# Title of the Streamlit app
st.title('YouTube to MP4 Downloader')

# Input field for YouTube URL
video_url = st.text_input('Enter YouTube video URL')

if st.button('Download MP4'):
    if not video_url:
        st.error("Please enter a YouTube video URL.")
    elif not is_valid_youtube_url(video_url):
        st.error("Please enter a valid YouTube URL.")
    else:
        try:
            # Get video object from pytube
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()

            # Download the video to a temp location
            video_path = stream.download()

            # Provide download button for the user
            with open(video_path, 'rb') as file:
                st.download_button(
                    label="Download MP4",
                    data=file,
                    file_name=f"{yt.title}.mp4",
                    mime="video/mp4"
                )

            # Optionally, clean up the file after download
            os.remove(video_path)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
