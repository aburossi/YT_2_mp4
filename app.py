import yt_dlp
import streamlit as st

video_url = st.text_input('Enter YouTube video URL')

if st.button('Download MP4'):
    if video_url:
        try:
            # Set up download options
            ydl_opts = {
                'format': 'best',
                'outtmpl': '/tmp/%(title)s.%(ext)s',
                'cookiefile': '/path_to_your_cookies/cookies.txt',  # Path to your exported cookies
            }

            # Download video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_title = info_dict.get('title', None)

            # Path to downloaded video
            video_path = f"/tmp/{video_title}.mp4"

            # Provide download button
            with open(video_path, 'rb') as file:
                st.download_button(
                    label="Download MP4",
                    data=file,
                    file_name=f"{video_title}.mp4",
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"Error downloading video: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
