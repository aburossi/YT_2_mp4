import streamlit as st
from pytube import YouTube
import os

# Title of the Streamlit app
st.title('YouTube to MP4 Downloader')

# Input field for YouTube URL
video_url = st.text_input('Enter YouTube video URL')

if st.button('Download MP4'):
    if video_url:
        try:
            # Get video object from pytube
            yt = YouTube(video_url)
            # Select the highest resolution stream available
            stream = yt.streams.get_highest_resolution()

            # Download the video to a temp location
            video_path = stream.download()

            # Once downloaded, provide a download button for the user
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
            st.error(f"Error: {str(e)}")
    else:
        st.warning('Please enter a valid YouTube URL.')

