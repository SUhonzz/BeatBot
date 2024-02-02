from classes import Song

# Create a few dummy songs
song1 = Song(song_id="1", artist="The Beatles", title="Yesterday", album="Help")
song2 = Song(song_id="2", artist="The Beatles", title="Hey Jude", album="Beatlejuice")
song3 = Song(song_id="3", artist="The Beatles", title="Let It Be", album="Beat me to it")

#song1.hash_audio("nevergonna.mp3")

song1.store_data()
song2.store_data()
song3.store_data()