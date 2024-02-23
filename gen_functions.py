import abracadabra.fingerprint as fp
from classes import Song,Hash
from tinydb import TinyDB, Query
import pyaudio
import wave
import streamlit as st
from pytube import YouTube
import lyricsgenius

def generate_hashes(audiofile, ytlink=None):
    hashes = fp.fingerprint_file(audiofile, ytlink)
    return hashes

def store_song(song,hashes):
    result = Song.store_data(song,hashes)
    return result
    #print(f"Song inserted from functions, song id = {song.song_id}")

def recognize(hashes):
    hashes = [_hash[0] for _hash in hashes]
    matches = {}

    result = Hash.load_data_by_hash(hashes[0])
    '''
    for _hash in hashes:
        result = Hash.load_data_by_hash(_hash)'''
    if result:
        if result.song_id in matches:
            matches[result.song_id] += 1
        else:
            matches[result.song_id] = 1
    return matches

        
def get_song_info(song_id):
   
    db = TinyDB('hashesDB.json')
    SongQuery = Query()
    result = db.table('songs').search(SongQuery.song_id == song_id)
    db.close()

    if result:
        song = result[0]
        return song['artist'], song['title'], song['album']
    else:
        print("Song ID not found in the database.")
        return None, None, None  # Return None values if the song ID is not found
    
def record_audio(output_file, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    st.info("Recording...")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.info("Recording stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def manage_recognitions(song_id, artist, title, album):
    # Open or create the TinyDB instance
    db = TinyDB('hashesDB.json')

    recognitions_table = db.table('recognitions')

    new_entry = {'song_id': song_id, 'artist': artist, 'title': title, 'album': album}
    recognitions_table.insert(new_entry)

    #while len(recognitions_table) > 5:
       # oldest_entry = recognitions_table.get(doc_id=1)
        #recognitions_table.remove(doc_ids=[oldest_entry.doc_id])

    # Close the database connection
    db.close()

def download_audio(youtube_link, output_path):
    try:
        yt = YouTube(youtube_link)
        audio_stream = yt.streams.filter(only_audio=True).first()

        audio_stream.download(output_path=output_path, filename='ytaudio.mp3')

        return True

    except Exception as e:
        print("Error:", e)
        return False


def search_song_lyrics(song_name):
    genius = lyricsgenius.Genius("ZHaNbqi587eKsCo6ciC1w9yzBcHb09DSSOJmXzRTgqbQUNXEc_RAxrkZPXf21jmC")
    song = genius.search_song(song_name)
    if song:
        return song.lyrics
    else:
        return None