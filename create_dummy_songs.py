from classes import Song, Hash
from gen_functions import *
# Create a few dummy songs
song1 = Song(artist="Rick Astley", title="Never Gonna Give You Up", album="Whenever You Need Somebody")
song2 = Song(artist="Zelda", title="Lorule Main", album="Link Between Worlds")

song1.song_id = store_hashes("nevergonna.mp3")
print(song1)
#song1.store_data()
#song2.store_data()
