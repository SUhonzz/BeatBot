import pandas as pd
import streamlit as st
# import streamlit_scrollable_textbox as stx

from classes import Song, Hash
from gen_functions import *
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from duckduckgo_search import DDGS

st.set_page_config(layout="wide", page_title="Harmonee", page_icon=":musical_note:")
st.image('./design/logo_v4.png', width=250)

col1, col2 = st.columns([0.6, 0.4])
artist, title = None, None

with col1:
    tab_learn, tab_recognize, tab_about = st.tabs(['Teach Songs', 'Recognize Songs', 'About'])

    with tab_learn:

        st.header("Teach new Songs")
        with st.container(border=True):
            ytupload = st.toggle('Load from YouTube', key='yt')
        with st.container(border=True):
            if ytupload:
                yt_link = st.text_input("Or paste a YouTube link to load the audio",
                                        placeholder="Insert YouTube link")
                if st.button('Load'):
                    if download_audio(yt_link, "./"):
                        st.success("Youtube-Audio loaded successfully")
                    else:
                        st.error("Error loading Youtube-Audio, please check the link and try again")

                try:
                    st.write("Last Loaded Audio:")
                    st.audio('ytaudio.mp3', format='audio/wav')
                    uploaded_file = 'ytaudio.mp3'
                except:
                    st.warning("No audio file loaded yet")
            else:
                uploaded_file = st.file_uploader("Upload a song to learn", type=["mp3", "wav"],
                                                 accept_multiple_files=False)
                if uploaded_file is not None:
                    st.audio(uploaded_file, format='audio/wav')

        with st.form(key='teach_new_song', border=True):
            song_title = st.text_input("Song Title")
            song_artist = st.text_input("Artist")
            song_album = st.text_input("Album")

            if st.form_submit_button('Teach'):
                if uploaded_file is not None and song_title != "" and song_artist != "" and song_album != "":
                    if ytupload:
                        hashes = generate_hashes(uploaded_file, yt_link)
                    else:
                        hashes = generate_hashes(uploaded_file)
                    new_song = Song(artist=song_artist, title=song_title, album=song_album)
                    new_song.song_id = hashes[0][2]
                    print("Hashes stored")
                    if store_song(new_song, hashes):
                        st.success("Song stored successfully")
                        print("Song stored")
                        st.rerun()
                    else:
                        st.warning("Song already exists in the database")
                else:
                    st.error("Please upload a song to learn and fill in all the fields.")

    with tab_recognize:
        st.header("Recognize Songs from Snippet")
        with st.container(border=True):
            uploaded_snippet = st.file_uploader("Upload a snippet to recognise", type=["mp3", "wav"])
            if uploaded_snippet is not None:
                st.audio(uploaded_snippet, format='audio/wav')

            if st.button('Recognize'):
                if uploaded_snippet is not None:
                    hashes = generate_hashes(uploaded_snippet)
                    matches = recognize(hashes)
                    if len(matches) == 0:
                        st.error("No matches found, either teach the song or upload a different snippet.")
                    for key in matches:
                        # st.write(f"Song ID: {key}, Matches: {matches[key]}")

                        artist, title, album = get_song_info(key)
                        if artist is not None:
                            st.success(f"Artist: {artist}, Title: {title}, Album: {album}")
                            manage_recognitions(key, artist, title, album)
                        else:
                            print("Song ID not found in the database.")

                else:
                    st.error("Please upload a snippet to recognize")

        st.header("Recognize from Microphone")

        with st.container(border=True):
            if st.button('Start Recording'):
                record_audio('temp.wav', 10)
                st.success("Recording complete")
                st.audio('temp.wav', format='audio/wav')
                hashes = generate_hashes('temp.wav')
                matches = recognize(hashes)
                if len(matches) == 0:
                    st.error("No matches found, either teach the song or try recording again.")
                for key in matches:
                    # st.write(f"Song ID: {key}, Matches: {matches[key]}")

                    artist, title, album = get_song_info(key)
                    if artist is not None:
                        st.success(f"Artist: {artist}, Title: {title}, Album: {album}")
                        manage_recognitions(key, artist, title, album)

                    else:
                        print("Song ID not found in the database.")
    with tab_about:
        st.header("About Harmonee")
        st.write(
            "**Harmonee** is a song recognition app that uses audio fingerprinting to recognize songs. It uses a Fingerprinting algorithm to generate hashes from audio files and stores them in a database. When a snippet is uploaded, it generates hashes from the snippet and compares them to the database to find a match. It can also record audio from the microphone and recognize songs from it.")
        st.write(
            "**Harmonee** is built using Python and Streamlit. It uses the *abracadabra* audio-recognizing-library as a base for audio fingerprinting and several other libraries like *pydub, pyaudio* or *lyricsgenius* for additional functionality. The database is managed using *TinyDB*, The album covers displayed on recognition are integrated through *DuckDuckGo-search*. Lyrics are loaded from *Genius.com*.")
        st.write(
            "The source code for abracadabra is available on GitHub at https://github.com/notexactlyawe/abracadabra")
        st.write(
            "Harmonee is developed by Andreas Thöni, Samuel Peer and Hannes Unterhuber as part of the final project for the course *Introduction to Softwaredesign* at the MCI Innsbruck.")
        st.write(
            "The absolute mess of a source code for **Harmonee** is available on GitHub at https://github.com/SUhonzz/Harmonee")

with col2:
    st.header("History")
    links, rechts = st.columns([1, 1])
    with links:
        st.subheader("Last 5 taught songs")
        with st.expander("Show last 5 taught songs"):
            taught_df = pd.DataFrame(columns=['Title', 'Artist', 'Album'])
            db = TinyDB('hashesDB.json')
            songs = db.table('songs')
            result = songs.all()
            for i in range(len(result) - 1, len(result) - 6, -1):
                # st.write(f"Title: {result[i]['title']}, Artist: {result[i]['artist']},  Album: {result[i]['album']}, Song ID: {result[i]['song_id']}")
                taught_df.loc[len(taught_df)] = [result[i]['title'], result[i]['artist'], result[i]['album']]
            db.close()
            st.dataframe(taught_df, hide_index=True)
    with rechts:
        st.subheader("Last 5 recognized songs")
        with st.expander("Show last 5 recognized songs"):
            rec_df = pd.DataFrame(columns=['Title', 'Artist', 'Album'])
            db = TinyDB('hashesDB.json')
            recognitions = db.table('recognitions')
            result = recognitions.all()
            for i in range(len(result) - 1, len(result) - 6, -1):
                # st.write(f"Title: {result[i]['title']}, Artist: {result[i]['artist']},  Album: {result[i]['album']}, Song ID: {result[i]['song_id']}")
                rec_df.loc[len(rec_df)] = [result[i]['title'], result[i]['artist'], result[i]['album']]
            db.close()
            st.dataframe(rec_df, hide_index=True)

    st.header("Song Info")
    if artist is not None and title is not None:
        if artist is not None and title is not None:
            prompt = F'{title} {artist} album cover'
            with DDGS() as ddgs:
                keywords = prompt
                ddgs_images_gen = ddgs.images(
                    keywords,
                    region="wt-wt",
                    safesearch="off",
                    size=None,
                    type_image=None,
                    layout=None,
                    license_image=None,
                    max_results=1,
                )
                for r in ddgs_images_gen:
                    pass

                with st.container(border=True):
                    cover, info = st.columns([0.5, 0.5])
                    with cover:
                        st.image(r['image'], caption=r['title'], use_column_width=True)
                    with info:
                        with st.container(border=True):
                            st.subheader('Artist')
                            st.write(f"{artist}")
                        with st.container(border=True):
                            st.subheader('Title')
                            st.write(f"{title}")
                        with st.container(border=True):
                            st.subheader('Album')
                            st.write(f"{album}")

    else:
        with st.container(border=True):
            cover, info = st.columns([0.5, 0.5])
            with cover:
                st.image('./design/no_album_static.png', caption='No Matched Song', use_column_width=True,
                         output_format='PNG')
            with info:
                with st.container(border=True):
                    st.subheader('Artist')
                    st.write('No Matched Song')
                with st.container(border=True):
                    st.subheader('Title')
                    st.write('No Matched Song')
                with st.container(border=True):
                    st.subheader('Album')
                    st.write('No Matched Song')

    with st.expander('**Lyrics** *(powered by Genius.com)*'):
        if artist is not None and title is not None:
            lyrics = search_song_lyrics(f'{title} {artist}')
        else:
            lyrics = None
        if lyrics:
            # stx.scrollableTextbox(lyrics, height=300)
            st.text(lyrics)
        else:
            st.warning("No lyrics found for this song")






