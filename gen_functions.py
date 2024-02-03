import abracadabra.fingerprint as fp
from classes import Song, Hash


def store_hashes(audiofile):
    hashes = fp.fingerprint_file(audiofile)
    for hashsin in hashes:
        new_hash = Hash(hash=hashsin[0], song_id=hashsin[2], offset=hashsin[1])
        #print(new_hash)
        new_hash.store_data()
    return hashes[0][2]

def print_hashes(audiofile):
    hashes = fp.fingerprint_file(audiofile)
    print(hashes)