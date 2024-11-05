from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys


ON_REPEAT_PLAYLIST_URI = "spotify:playlist:37i9dQZF1EpiwFDq6VvF8I"

# spotify authentication with required scopes (picks up client id/secret as env variables)
scope = "playlist-read-private playlist-modify-private playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
    )
)


def create_on_repeat_archive():
    try:
        # TODO: get last month not current month
        playlist_name = datetime.now().strftime("%b %y")

        on_repeat_tracks = sp.playlist_tracks(ON_REPEAT_PLAYLIST_URI)["items"]

        track_uris = [track["track"]["uri"] for track in on_repeat_tracks]

        # create new playlist
        user_id = sp.current_user()["id"]
        new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        new_playlist_id = new_playlist["id"]

        # add tracks
        sp.playlist_add_items(new_playlist_id, track_uris)
        print(f"Archived 'On Repeat' playlist to '{playlist_name}'")

    except Exception as error:
        sys.exit(f"An error occurred creating playlist: {error}")


if __name__ == "__main__":
    create_on_repeat_archive()
