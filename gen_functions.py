import abracadabra.fingerprint as fp
from classes import Song,Hash

def generate_hashes(audiofile):
    hashes = fp.fingerprint_file(audiofile)
    return hashes

def store_song(song,hashes):
    Song.store_data(song,hashes)
    print(f"Song inserted from functions, song id = {song.song_id}")

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

def match_id_to_song(song_id):
    for song in Song.db_connector_h:
        if song.song_id == song_id:
            return song