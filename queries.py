import os
from tinydb import TinyDB, Query
from serializer import serializer


def find_songs() -> list:
    """Find all songs in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('songs')
    # Create a query object
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["title"] for x in result]
    return result

