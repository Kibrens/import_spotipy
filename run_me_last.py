import time
from spotipy.exceptions import SpotifyException
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

######################################################################################################################
# Your Spotify Developer credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:8888/callback'  # This URI must match what you set in the Spotify Developer Dashboard

playlist_name = "My artists Playlist"  # Change this to the name of your existing playlist
YOUR_FILE = "./output_artists.txt"  # <------------------ Path to your text file
######################################################################################################################

# Authentication and creating a spotipy object with a custom timeout
def authenticate_spotify():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-public playlist-modify-private user-library-read"))

# Function to clean the song names (strip unwanted characters and fix encoding issues)
def clean_song_name(song):
    # Strip any unwanted characters (e.g., null characters)
    song = song.strip()
    # Ensure the song name is correctly encoded (UTF-8)
    return song.encode('utf-8', 'ignore').decode('utf-8')
# Function to search and get song URIs from the list of song names in batches
def get_song_uris_batch(sp, song_list, playlist_id, batch_size=20):
    uris = []
    for i in range(0, len(song_list), batch_size):
        batch = song_list[i:i+batch_size]
        batch_uris = []
        
        for song in batch:
            cleaned_song = clean_song_name(song)
            result = sp.search(q=cleaned_song, limit=1, type='track', market='US')
            if result['tracks']['items']:
                batch_uris.append(result['tracks']['items'][0]['uri'])
            else:
                print(f"Song not found: {cleaned_song}")

        uris.extend(batch_uris)
        print(f"Processed batch {i//batch_size + 1} of {len(song_list) // batch_size + 1}")
        
        # Add the batch to the playlist
        add_songs_to_playlist(sp, playlist_id, batch_uris)
        
        # Refresh the connection after every 50 batches
        if (i // batch_size + 1) % 50 == 0:
            print("Refreshing connection...")
            time.sleep(5)  # Optional: Add a slight delay before re-authenticating
            sp = authenticate_spotify()  # Re-authenticate and create a new Spotify object
    # return uris
# Create a playlist
def create_playlist(sp, user_id, playlist_name):
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = playlist['id']

# Function to get an existing playlist by name
def get_playlist_id_by_name(playlist_name):
    playlists = sp.current_user_playlists()['items']
    for playlist in playlists:
        if playlist['name'] == playlist_name:
            return playlist['id']
    return None  # If the playlist wasn't found

# Function to add songs to an existing playlist
def add_songs_to_playlist(sp, playlist_id, uris):
    sp.playlist_add_items(playlist_id, uris)

# Read song list from a file
def read_song_list(file_path):
    with open(file_path, 'r', encoding='utf-16') as f:  # Ensure UTF-16 encoding when reading the file
        songs = f.readlines()
    return [song.strip() for song in songs]

if __name__ == "__main__":
    # Authenticate Spotify
    sp = authenticate_spotify()

    # Get the current user's Spotify ID
    user_id = sp.current_user()['id']

    # Get the playlist ID of the existing playlist (replace with your playlist name)
    playlist_id = get_playlist_id_by_name(playlist_name)
    
    if not playlist_id:
        # If the playlist doesn't exist, create it
        playlist_id = create_playlist(sp, user_id, playlist_name)

    # Read the songs from your text file
    read_song_list(YOUR_FILE)
    song_uris = get_song_uris_batch(sp, song_list, playlist_id)
    
