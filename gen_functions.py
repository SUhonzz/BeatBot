import abracadabra.fingerprint as fp
from classes import Song, Hash


def store_hashes(audiofile):
    hashes = fp.fingerprint_file(audiofile)
    hashes_to_insert = []

    for hashsin in hashes:
        new_hash = Hash(hash=hashsin[0], song_id=hashsin[2], offset=hashsin[1])
        hashes_to_insert.append(new_hash.__dict__)
        #print(new_hash)
    Hash.db_connector_h.insert_multiple(hashes_to_insert)
    return hashes[0][2]


def recognize(hashes):
    matches = {}
    for hashsin in hashes:
        result = Hash.load_data_by_hash(hashsin)
        if result:
            if result.song_id in matches:
                matches[result.song_id] += 1
            else:
                matches[result.song_id] = 1
    return matches


def print_hashes(audiofile):
    hashes = fp.fingerprint_file(audiofile)
    print(hashes)