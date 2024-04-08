import time
import boto3
from threading import Thread
from data_ingestion import data_ingestion
from process_events import consume_events

if __name__ == "__main__":
    kinesis_client = boto3.client("kinesis", region_name="us-east-1")
    stream_name = "event-stream"  # Update with your actual stream name
    s3_bucket = 'babbel-streaming-bucket'
    s3_prefix = 'raw'

    # Set the duration for running the ingestion script (5 minutes)
    duration_in_minutes = 1
    start_time = time.time()
    end_time = start_time + (duration_in_minutes * 60)

    # Define the functions to run
    def run_data_ingestion():
        while time.time() < end_time:
            print("Running data ingestion into kinesis")
            data_ingestion(kinesis_client, stream_name, end_time)
            time.sleep(1)  # Adjust the interval as needed
        print("Completed data ingestion into kinesis")

    def run_consume_events():
        while time.time() < end_time:
            consume_events(stream_name, s3_bucket, s3_prefix, end_time)

    # Create threads for each function
    data_ingestion_thread = Thread(target=run_data_ingestion)
    consume_events_thread = Thread(target=run_consume_events)

    # Start both threads
    data_ingestion_thread.start()
    consume_events_thread.start()

    # Wait for both threads to finish
    data_ingestion_thread.join()
    consume_events_thread.join()

    print("Both tasks have completed.")
