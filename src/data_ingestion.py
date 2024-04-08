import json
import time
import random
import uuid

def data_ingestion(kinesis_client, stream_name, end_time):
    event_types = ["account:created", "lesson:started", "payment:order:completed", "lesson:completed",
                   "quiz:started", "quiz:completed",
                   "lesson:failed", "quiz:failed", "achievement:unlocked",
                   "level:up", "streak:lost", "streak:regained",
                   "language:switched", "badge:earned",
                   "leaderboard:position:changed", "lesson:repeated",
                   "quiz:skipped", "lesson:completed:bonus",
                   "challenge:issued", "challenge:accepted",
                   "challenge:completed", "resource:unlocked", "resource:locked"]

    while time.time() < end_time:
        event_uuid = str(uuid.uuid4())
        event_name = random.choice(event_types)
        created_at = int(time.time())

        event = {
            "event_uuid": event_uuid,
            "event_name": event_name,
            "created_at": created_at,
            "payload": {
                "example_key": "example_value"
            }
        }

        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(event),
            PartitionKey=event_uuid
        )

        print(f"Put record to Kinesis stream: {response['SequenceNumber']}")
