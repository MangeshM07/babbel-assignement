import json
import time
from datetime import datetime
import boto3
import pandas as pd

# Set to store unique event identifiers
unique_events = set()


def process_event(event):
    # Parse JSON object
    event_data = json.loads(event['Data'])

    # Extract common fields
    event_uuid = event_data['event_uuid']
    event_name = event_data['event_name']
    created_at = event_data['created_at']

    # Check if event is a duplicate based on event uuid and created_at
    event_identifier = (event_uuid, created_at)
    if event_identifier in unique_events:
        print(f"Duplicate event found and skipped: {event_identifier}")
        return None

    # Add event identifier to set
    unique_events.add(event_identifier)

    # Calculate additional fields
    created_datetime = datetime.fromtimestamp(created_at).isoformat()
    event_type, event_subtype = event_name.split(':')[:2]

    # Add additional fields to event data
    event_data['created_datetime'] = created_datetime
    event_data['event_type'] = event_type
    event_data['event_subtype'] = event_subtype

    return event_data


def consume_events(stream_name, s3_bucket, s3_prefix, end_time):
    kinesis = boto3.client('kinesis')

    # Get list of all shard IDs in the stream
    shard_ids = kinesis.list_shards(StreamName=stream_name)['Shards']

    for shard in shard_ids:
        shard_iterator = kinesis.get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard['ShardId'],
            ShardIteratorType='LATEST'
        )['ShardIterator']

        while shard_iterator and time.time() < end_time:
            response = kinesis.get_records(ShardIterator=shard_iterator, Limit=100)
            records = []
            for record in response['Records']:
                event_data = process_event(record)
                if event_data:
                    records.append(event_data)

            if records:
                # Create DataFrame from processed events
                events_df = pd.DataFrame(records)

                # Write DataFrame to Parquet format partitioned by event type in S3
                for event_type, group in events_df.groupby('event_type'):
                    s3_path = f"s3://{s3_bucket}/{s3_prefix}/{event_type}"
                    group.to_parquet(f"{s3_path}/data.parquet")
                    print(f"Stored processed events in Parquet format in S3: {s3_path}")

            shard_iterator = response.get('NextShardIterator')

        if time.time() >= end_time:  # Check if current time exceeds end_time
            print("Exiting consume_events as duration exceeded.")
            break
