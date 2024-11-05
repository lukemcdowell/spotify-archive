import json
from main import create_on_repeat_archive


def lambda_handler(event, context):
    try:
        create_on_repeat_archive()
        # TODO: email on success

        return {"statusCode": 200, "body": json.dumps("Playlist created successfully!")}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Failed to create playlist: {str(e)}"),
        }
