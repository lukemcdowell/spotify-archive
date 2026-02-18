from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct
import os

class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        fn = PythonFunction(
            self, "SpotifyArchiveFn",
            runtime=_lambda.Runtime.PYTHON_3_12,
            entry="lambda",
            index="handler.py",
            handler="handler",
            timeout=Duration.seconds(120),
            environment={
                "ALERT_EMAIL_ADDRESS": os.environ["ALERT_EMAIL_ADDRESS"],
                "ALERT_EMAIL_PASSWORD": os.environ["ALERT_EMAIL_PASSWORD"],
                "EMAIL_ADDRESS": os.environ["EMAIL_ADDRESS"],
                "SPOTIPY_CLIENT_ID": os.environ["SPOTIPY_CLIENT_ID"],
                "SPOTIPY_CLIENT_SECRET": os.environ["SPOTIPY_CLIENT_SECRET"],
                "SPOTIPY_REDIRECT_URI": os.environ["SPOTIPY_REDIRECT_URI"]
            }
        )

        rule = events.Rule(
            self,
            "SpotifyArchiveMonthlySchedule",
            schedule=events.Schedule.cron(
                minute="0",
                hour="1",
                day="1"
            ),
        )

        rule.add_target(targets.LambdaFunction(fn))
