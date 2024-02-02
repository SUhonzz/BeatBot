import streamlit as st
from classes import Song

st.set_page_config(layout="wide", page_title="Harmonee", page_icon=":musical_note:")
st.image('./logo_v4.png', width=250)

col1,col2 = st.columns([0.6, 0.4])

with col1:
    tab_learn, tab_recognize = st.tabs(['Teach Songs', 'Recognize Songs'])

    with tab_learn:


        
        st.header("Teach new Songs")
        with st.form(key='teach_new_song', border=True):
            song_title = st.text_input("Song Title")
            song_artist = st.text_input("Artist")
            song_album = st.text_input("Album")
            uploaded_file = st.file_uploader("Upload a song to learn", type=["mp3", "wav"], accept_multiple_files=False)
            if uploaded_file is not None:
                st.audio(uploaded_file, format='audio/wav')


            if st.form_submit_button('Teach'):
                if uploaded_file is not None:
                    new_song = Song(song_id="1", artist=song_artist, title=song_title, album=song_album)
                    new_song.hash_audio(uploaded_file.name)
                    new_song.store_data()
                    st.rerun()
                else:
                    st.error("Please upload a song to learn")
                
                    

    with tab_recognize:
        st.header("Recognize Songs")
        uploaded_snippet = st.file_uploader("Upload a snippet to recognise", type=["mp3", "wav"])