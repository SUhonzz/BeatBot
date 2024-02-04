import streamlit as st
from classes import Song
from gen_functions import *

st.set_page_config(layout="wide", page_title="Harmonee", page_icon=":musical_note:")
st.image('./logo_v4.png', width=250)

col1, col2 = st.columns([0.6, 0.4])

with col1:
    tab_learn, tab_recognize = st.tabs(['Teach Songs', 'Recognize Songs'])

    with tab_learn:

        st.header("Teach new Songs")
        with st.container(border=True):
            uploaded_file = st.file_uploader("Upload a song to learn", type=["mp3", "wav"], accept_multiple_files=False)
            if uploaded_file is not None:
                st.audio(uploaded_file, format='audio/wav')

        with st.form(key='teach_new_song', border=True):
            song_title = st.text_input("Song Title")
            song_artist = st.text_input("Artist")
            song_album = st.text_input("Album")

            if st.form_submit_button('Teach'):
                if uploaded_file is not None:
                    new_song = Song(artist=song_artist, title=song_title, album=song_album)
                    new_song.song_id = store_hashes(uploaded_file.name)
                    new_song.store_data()
                    st.rerun()
                else:
                    st.error("Please upload a song to learn")

    with tab_recognize:
        st.header("Recognize Songs")
        with st.container(border=True):
            uploaded_snippet = st.file_uploader("Upload a snippet to recognise", type=["mp3", "wav"])
            if uploaded_snippet is not None:
                st.audio(uploaded_snippet, format='audio/wav')

            if st.button('Recognize'):
                if uploaded_snippet is not None:
                    hashes = fp.fingerprint_file(uploaded_snippet.name)
                    matches = recognize(hashes)

                    for key in matches:
                        st.write(f"Song ID: {key}, Matches: {matches[key]}")

                else:
                    st.error("Please upload a snippet to recognize")
