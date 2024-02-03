import abracadabra.fingerprint as fp
from tinydb import TinyDB, Query
from serializer import serializer
import os


class Hash:
    db_connector_h = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hashes.json'), storage=serializer).table('hashes')

    def __init__(self, hash=None, offset=None, song_id=None):
        self.hash = hash
        self.offset = offset
        self.song_id = song_id

    def store_data(self):
        # Check if the device already exists in the database
        HashQuery = Query()
        result = self.db_connector_h.search(HashQuery.hash == self.hash)
        #data_to_store = {'title': self.title, 'id': self.id}
        if result:
            # Update the existing record with the current instance's data
            self.db_connector_h.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Hash updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector_h.insert(self.__dict__)
            print("Hash inserted.")

    @classmethod
    def load_data_by_hash(cls, hash):
        # Load data from the database and create an instance of the Hash class
        HashQuery = Query()
        result = cls.db_connector_h.search(HashQuery.hash == hash)

        if result:
            doc_index = result[0].doc_id
            data = result[0]
            return cls(data['hash'], data['offset'], data['song_id'])
        else:
            return None

    def __str__(self):
        return f"Hash: {self.hash}, Offset: {self.offset}, Song ID: {self.song_id}"


class Song:
    db_connector_s = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'songs.json'), storage=serializer).table('songs')
    
    def __init__(self, song_id=None, artist=None, title=None, album=None):
        # Generate unique ID for the song based on title
        #self.song_id = abs(hash(title)) % (10 ** 6)
        self.song_id = song_id
        self.artist = artist
        self.title = title
        self.album = album

    #def hash_audio(self, audiofile=None):
        #self.hashes = fp.fingerprint_file(audiofile)

    def store_data(self):
        print("Storing data...")
        # Check if the song already exists in the database
        SongQuery = Query()
        result = self.db_connector_s.search(SongQuery.title == self.title)
        #data_to_store = {'title': self.title, 'id': self.id}
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector_s.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Songs updated.")
        else:
            # If the song doesn't exist, insert a new record
            self.db_connector_s.insert(self.__dict__)
            print("Songs inserted.")
    
    @classmethod
    def load_data_by_title(cls, title):
        # Load data from the database and create an instance of the Device class
        SongQuery = Query()
        result = cls.db_connector_s.search(SongQuery.title == title)

        if result:
            doc_index = result[0].doc_id
            data = result[0]
            return cls(data['song_id'], data['artist'], data['title'], data['album'])
        else:
            return None

    def __str__(self):
        return f"Song ID: {self.song_id}, Artist: {self.artist}, Title: {self.title}, Album: {self.album}"