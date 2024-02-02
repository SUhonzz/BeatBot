import abracadabra.fingerprint as fp
from tinydb import TinyDB, Query
from serializer import serializer
import os

class Song:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('songs')
    
    def __init__(self, song_id=None, artist=None, title=None, album=None, hashes=None, offset=0):
        self.song_id = song_id
        self.artist = artist
        self.title = title
        self.album = album
        self.hashes = hashes
        self.offset = offset

    def hash_audio(self, audiofile=None):
        self.hashes = fp.fingerprint_file(audiofile)

    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        SongQuery = Query()
        result = self.db_connector.search(SongQuery.title == self.title)
        #data_to_store = {'title': self.title, 'id': self.id}
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Songs updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Songs inserted.")
    
    @classmethod
    def load_data_by_title(cls, title):
        # Load data from the database and create an instance of the Device class
        SongQuery = Query()
        result = cls.db_connector.search(SongQuery.title == title)

        if result:
            doc_index = result[0].doc_id
            data = result[0]
            return cls(data['song_id'], data['artist'], data['title'], data['album'], data['hashes'], data['offset'])
        else:
            return None