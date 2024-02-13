import abracadabra.fingerprint as fp
from tinydb import TinyDB, Query
from serializer import serializer
import os

class Song:

    db_connector_h = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hashesDB.json'), storage=serializer).table('songs')

    def __init__(self, song_id=None, artist=None, title=None, album=None):
        self.song_id = song_id
        self.artist = artist
        self.title = title
        self.album = album

    def store_hashes(self,hashes):
        hashes_to_insert = []

        for hashsin in hashes:
            new_hash = Hash(hash=hashsin[0], song_id=hashsin[2], offset=hashsin[1])
            hashes_to_insert.append(new_hash.__dict__)
        Hash.db_connector_h.insert_multiple(hashes_to_insert)
        

   
    def store_data(self,hashes):
        # Check if the device already exists in the database
        HashQuery = Query()
        result = self.db_connector_h.search(HashQuery.song_id == self.song_id)
        
        if len(result) != 0:
            print("Song already exists in the database from classes")
            
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector_h.insert({'song_id':self.song_id,'artist':self.artist,'title':self.title,'album':self.album})
            self.store_hashes(hashes)
            print("Song inserted from classes")
            

    


class Hash:

    db_connector_h = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hashesDB.json'), storage=serializer).table('hashes')

    def __init__(self, hash=None, offset=None, song_id=None):
        self.hash = hash
        self.offset = offset
        self.song_id = song_id
    
    def store_data(self,data_to_store):
        # Check if the device already exists in the database
        HashQuery = Query()
        result = self.db_connector_h.search(HashQuery.hash == data_to_store.hash)
        #data_to_store = {'title': self.title, 'id': self.id}
        if len(result) != 0:
            # Update the existing record with the current instance's data
            #self.db_connector_h.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Hashes already exists in the database from classes")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector_h.insert_multiple(data_to_store)
            print("Hash inserted from classes")

    @classmethod
    def load_data_by_hash(cls, hash_list):
        # Load data from the database and create an instance of the Hash class
        HashQuery = Query()
        result = cls.db_connector_h.search(HashQuery.hash.one_of([hash_list]))

        if result:
            doc_index = result[0].doc_id
            data = result[0]
            return cls(data['hash'], data['offset'], data['song_id'])
        else:
            return None

    def __str__(self):
        return f"Hash: {self.hash}, Offset: {self.offset}, Song ID: {self.song_id}"
