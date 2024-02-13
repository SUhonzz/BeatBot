import streamlit as st
from classes import Song,Hash
from gen_functions import *
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from duckduckgo_search import DDGS

st.set_page_config(layout="wide", page_title="Harmonee", page_icon=":musical_note:")
st.image('./logo_v4.png', width=250)

col1, col2 = st.columns([0.6, 0.4])
artist, title = None, None

with col1:
    tab_learn, tab_recognize, tab_about = st.tabs(['Teach Songs', 'Recognize Songs','About'])

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
                filename = f"./Samples/{uploaded_file.name}"
                hashes = generate_hashes(filename)
                if uploaded_file is not None:
                    print(uploaded_file.name)
                    new_song = Song(artist=song_artist, title=song_title, album=song_album)
                    new_song.song_id = hashes[0][2]
                    print("Hashes stored")
                    store_song(new_song,hashes)
                    print("Song stored")
                    st.rerun()
                    
                else:
                    st.error("Please upload a song to learn")

    with tab_recognize:
        st.header("Recognize Songs from Snippet")
        with st.container(border=True):
            uploaded_snippet = st.file_uploader("Upload a snippet to recognise", type=["mp3", "wav"])
            if uploaded_snippet is not None:
                st.audio(uploaded_snippet, format='audio/wav')

            if st.button('Recognize'):
                if uploaded_snippet is not None:
                    snippet_path = f"./Samples/Cutlets/{uploaded_snippet.name}"
                    hashes = generate_hashes(snippet_path)
                    matches = recognize(hashes)
                    if len(matches) == 0:
                        st.error("No matches found, either teach the song or upload a different snippet.")
                    for key in matches:
                       #st.write(f"Song ID: {key}, Matches: {matches[key]}")

                       artist, title, album = get_song_info(key)
                       if artist is not None:
                           st.write(f"Artist: {artist}, Title: {title}, Album: {album}")
                           manage_recognitions(key,artist,title,album)
                       else:
                            print("Song ID not found in the database.")

                else:
                    st.error("Please upload a snippet to recognize")

        st.header("Recognize from Microphone")

        with st.container(border=True):
            if st.button('Start Recording'):
                record_audio('temp.wav', 5)
                st.write("Recording complete")
                st.audio('temp.wav', format='audio/wav')
                hashes = generate_hashes('temp.wav')
                matches = recognize(hashes)
                if len(matches) == 0:
                    st.error("No matches found, either teach the song or upload a different snippet.")
                for key in matches:
                    #st.write(f"Song ID: {key}, Matches: {matches[key]}")

                    artist, title, album = get_song_info(key)
                    if artist is not None:
                        st.write(f"Artist: {artist}, Title: {title}, Album: {album}")
                        manage_recognitions(key,artist,title,album)
                        
                    else:
                        print("Song ID not found in the database.")
    with tab_about:
        st.header("About Harmonee")
        st.write("Harmonee is a song recognition app that uses audio fingerprinting to recognize songs. It uses the Fingerprinting algorithm to generate hashes from audio files and stores them in a database. When a snippet is uploaded, it generates hashes from the snippet and compares them to the database to find a match. It can also record audio from the microphone and recognize songs from it.")
        st.write("Harmonee is built using Python and Streamlit. It uses the Fingerprinting library for audio fingerprinting and the Pydub library for audio processing.")
        st.write("Special thanks to the authors of the abracadabra project, which was used as a base for the Fingerprinting algorithm. The source code for abracadabra is available on GitHub at https://github.com/notexactlyawe/abracadabra")
        st.write("Harmonee is developed by Andreas Thöni, Samuel Peer and Hannes Unterhuber as a part of the final project for the course Introduction to Softwaredesign at the MCI Innsbruck.")
        st.write("The source code for Harmonee is available on GitHub at https://github.com/SUhonzz/Harmonee")

with col2:
    st.header("History")
    links,rechts = st.columns([1,1])
    with links:
        st.subheader("Last 5 tought songs")
        with st.expander("Show last 5 tought songs"):
            db = TinyDB('hashesDB.json')
            songs = db.table('songs')
            result = songs.all()
            for i in range(len(result)-1,len(result)-6,-1):
                st.write(f"Title: {result[i]['title']}, Artist: {result[i]['artist']},  Album: {result[i]['album']}, Song ID: {result[i]['song_id']}")
            db.close()
    with rechts:
        st.subheader("Last 5 recognized songs")
        with st.expander("Show last 5 recognized songs"):
            db = TinyDB('hashesDB.json')
            recognitions = db.table('recognitions')
            result = recognitions.all()
            for i in range(len(result)-1,len(result)-6,-1):
                st.write(f"Title: {result[i]['title']}, Artist: {result[i]['artist']},  Album: {result[i]['album']}, Song ID: {result[i]['song_id']}")
            db.close()

    if artist is not None and title is not None:
        st.header("Song Info")
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
                    st.image(r['image'], caption=r['title'], width=300)
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






