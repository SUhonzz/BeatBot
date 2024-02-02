import streamlit as st

st.set_page_config(layout="wide", page_title="Harmonee", page_icon=":musical_note:")
st.image('./logo_v4.png', width=250)

col1,col2 = st.columns([0.6, 0.4])

with col1:
    tab_learn, tab_recognize = st.tabs(['Teach Songs', 'Recognize Songs'])

    with tab_learn:
        st.header("Teach new Songs")
        uploaded_file = st.file_uploader("Upload a song to learn", type=["mp3", "wav"])
        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')

    with tab_recognize:
        st.header("Recognize Songs")
        uploaded_snippet = st.file_uploader("Upload a snippet to recognise", type=["mp3", "wav"])