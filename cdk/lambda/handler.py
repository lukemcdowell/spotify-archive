from datetime import datetime, timedelta
import json
from mail import send_email
from main import create_top_tracks_archive


def handler(event, context):
    today = datetime.now()
    last_month = today - timedelta(weeks=1)
    playlist_name = last_month.strftime("%b %y")

    try:
        playlist_url = create_top_tracks_archive(playlist_name)
        send_email(
            "Top Track Archive",
            f"Top Track archive created: <a href={playlist_url}>{playlist_name}</a>",
        )

        return {"statusCode": 200, "body": json.dumps("Playlist created successfully!")}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Failed to create playlist: {str(e)}"),
        }


if __name__ == "__main__":
    print(handler("test", "test"))
