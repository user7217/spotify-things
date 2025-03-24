import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter

# Spotify Credentials
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "https://google.com"
PLAYLIST_ID = "4c8WfmI3tXmd1Mhc8SLyT9"

# Authenticate using SpotifyOAuth (Required for Modifying Playlists)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private"
))

def get_playlist_tracks(playlist_id):
    """Fetches all tracks (artist, name, URI) from the playlist."""
    tracks = []
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results["items"]:
            track = item["track"]
            if track:  # Ensure track exists
                artist = track["artists"][0]["name"]
                name = track["name"]
                uri = track["uri"]
                tracks.append((artist, name, uri))

        # Get next page if available
        results = sp.next(results) if results["next"] else None

    return tracks

def delete_songs_by_artist(playlist_id, artist_name):
    """Deletes all songs by a specific artist from the playlist."""
    tracks = get_playlist_tracks(playlist_id)
    
    # Extract only the track URIs for the given artist
    to_remove = [uri for artist, name, uri in tracks if artist.lower() == artist_name.lower()]

    if not to_remove:
        print(f"No songs found by {artist_name}")
        return

    try:
        # Batch deletion (Spotify API only allows 100 tracks per request)
        for i in range(0, len(to_remove), 100):
            sp.playlist_remove_all_occurrences_of_items(playlist_id, to_remove[i:i+100])
        print(f"Deleted {len(to_remove)} songs by {artist_name}")
    except Exception as e:
        print(f"Error deleting songs: {e}")

def get_artist_counts(playlist_id):
    """Fetches all tracks and counts songs by each artist."""
    artist_count = Counter()
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results["items"]:
            track = item["track"]
            if track:  # Ensure track exists
                artist = track["artists"][0]["name"]
                artist_count[artist] += 1

        # Get next page if available
        results = sp.next(results) if results["next"] else None

    return artist_count

# Fetch and sort artist song counts in ascending order
artist_counts = get_artist_counts(PLAYLIST_ID)
sorted_counts = sorted(artist_counts.items(), key=lambda x: x[1])
print(len(sorted_counts))
# Print sorted artist song counts
for artist, count in sorted_counts:
    print(f"{artist}: {count} songs")


# Fetch and display all tracks
songs = get_playlist_tracks(PLAYLIST_ID)
print(len(songs))
# for artist, name, uri in songs:
#     print(f"{artist} - {name} - {uri}")

# Delete all songs by the specified artist
# delete_songs_by_artist(PLAYLIST_ID, "DISTURBED")
