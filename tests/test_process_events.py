import json
from datetime import datetime
from src.process_events import process_event

def test_process_event():
    # Sample event data
    event_data = {
        "event_uuid": "123456",
        "event_name": "account:created",
        "created_at": 1629235179
    }

    # Mock Kinesis event
    kinesis_event = {
        "Data": json.dumps(event_data)
    }

    # Call process_event function
    processed_event = process_event(kinesis_event)

    # Expected output
    expected_output = {
        "event_uuid": "123456",
        "event_name": "account:created",
        "created_at": 1629235179,
        "created_datetime": "2021-08-18T15:59:39",
        "event_type": "account",
        "event_subtype": "created"
    }

    # Compare processed event with expected output
    assert processed_event == expected_output
