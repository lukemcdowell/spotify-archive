import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys


# spotify authentication with required scopes (picks up client id/secret as env variables)
scope = "user-top-read playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
    )
)


def create_top_tracks_archive(playlist_name):
    try:
        top_tracks = sp.current_user_top_tracks(30, time_range="short_term")["items"]

        track_uris = [track["uri"] for track in top_tracks]

        # create new playlist
        user_id = sp.current_user()["id"]
        new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        new_playlist_id = new_playlist["id"]

        # add tracks
        sp.playlist_add_items(new_playlist_id, track_uris)
        print(f"Archived Top Tracks to '{playlist_name}'")

        return new_playlist["external_urls"]["spotify"]

    except Exception as error:
        sys.exit(f"An error occurred creating playlist: {error}")


if __name__ == "__main__":
    create_top_tracks_archive('Test Top Tracks Playlist')
