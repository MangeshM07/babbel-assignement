# import pytest
from unittest.mock import MagicMock, patch,ANY
from src.data_ingestion import data_ingestion

# @pytest.fixture
def mock_kinesis_client():
    with patch('src.data_ingestion.boto3.client') as mock_kinesis_client:
        yield mock_kinesis_client

def test_data_ingestion(mock_kinesis_client):
    # Mock the put_record method of the Kinesis client
    mock_put_record = MagicMock()
    mock_kinesis_client.return_value.put_record = mock_put_record
    
    # Define sample stream name
    stream_name = "event-stream"
    
    # Call the data_ingestion function
    data_ingestion(mock_kinesis_client, stream_name)
    
    # Verify that put_record method of the Kinesis client is called with the correct arguments
    mock_put_record.assert_called_once_with(
        StreamName=stream_name,
        Data=ANY,  # Ignore the data content
        PartitionKey=ANY  # Ignore the partition key
    )

    # Additional debug output
    print("Called put_record with arguments:", mock_put_record.call_args_list)
