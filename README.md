# Event Streaming Data Lake Solution README

## Architecture Diagram

                           +-----------------------+
                           |                       |
                           |    Kinesis Stream     |
                           |                       |
                           +-----------------------+
                                       |
                                       | 1M events/hour
                                       |
                                       V
                           +-----------------------+
                           |                       |
                           |      Data Lake        |
                           |    (Amazon S3)        |
                           +-----------------------+
                                       |
                                       | Querying & Analysis
                                       |
                                       V
                           +-----------------------+
                           |                       |
                           |  Analytical Services  |
                           |    (e.g., Athena,     |
                           |      Redshift)        |
                           +-----------------------+


## Technologies Used

### AWS Services
- **Amazon Kinesis:** Used to ingest and process real-time streaming data from various sources.
- **Amazon S3:** Serves as the data lake storage for storing raw and processed event data.


### Python Libraries
- **boto3:** Python SDK for AWS, used for interacting with AWS services programmatically.
- **pandas:** Data manipulation and analysis library, used for processing and transforming data.
- **pytest:** Testing framework for writing and executing unit tests.

## Solution Overview

The proposed solution leverages AWS cloud services to build a scalable and cost-effective event streaming data lake. 

1. **Data Ingestion:** Events are ingested into Amazon Kinesis streams from various sources. Each event is a JSON object containing common fields such as event_uuid, event_name, and created_at.

2. **Event Processing:** The `process_event` function processes each incoming event to extract additional fields, calculate derived values, and check for duplicates. Processed events are then stored in an Amazon S3 bucket in Parquet format partitioned by event type.

3. **Data Storage:** Amazon S3 serves as the primary storage for both raw and processed event data. Raw events are stored in a designated S3 bucket, while processed events are partitioned by event type in another S3 bucket to facilitate efficient querying.

4. **Querying and Analysis:** Amazon Athena can be used for ad-hoc querying and analysis of data stored in the S3 data lake. Users can run SQL queries to gain insights into event data without the need for provisioning or managing infrastructure.

5. **Optional Analytics:** For more complex analytical queries and deeper insights, Amazon Redshift can be used as a data warehouse. Data can be loaded from the S3 data lake into Redshift for running SQL queries at scale.

## Design Questions

### How would you handle duplicate events?

Duplicate events are identified based on a unique event identifier composed of event_uuid and created_at fields. Each incoming event is checked against a set of unique event identifiers to determine if it's a duplicate. If a duplicate event is detected, it is skipped and not processed further.

### How would you partition the data to ensure good querying performance and scalability?

Processed event data is partitioned by event type in the S3 bucket. This partitioning strategy ensures that data is logically organized and stored in separate directories based on event type. By partitioning the data, queries can be efficiently scoped to specific event types, resulting in improved query performance and scalability.

### What format would you use to store the data?

Processed event data is stored in Parquet format, a columnar storage format optimized for analytics workloads. Parquet offers efficient compression, columnar storage, and predicate pushdown capabilities, making it well-suited for analytical queries. Additionally, Parquet files support partitioning, which further enhances query performance and data organization.

### How would you test the different components of your proposed architecture?


### How would you ensure the architecture deployed can be replicable across environments?

To ensure replicability across environments, infrastructure as code (IaC) tools such as Terraform can be used to define and provision the AWS resources needed for the architecture. By codifying infrastructure configuration, environments can be easily replicated, version-controlled, and automated, leading to consistent deployments across development, testing, and production environments.

### Would your proposed solution still be the same if the amount of events is 1000 times smaller or bigger?

The proposed solution is designed to scale efficiently based on the volume of events. If the volume of events changes significantly, adjustments may be needed in terms of resource provisioning, data processing pipelines, and query optimization. However, the overall architecture and components remain the same, providing flexibility to scale up or down based on workload demands.

### Would your proposed solution still be the same if adding fields / transforming the data is no longer needed?

If the requirement for adding fields or transforming data is no longer needed, the architecture can be simplified by removing the data processing component. In this case, events can be ingested directly into the data lake without additional processing, reducing complexity and overhead. The choice of storage format and querying mechanism may also be adjusted based on the new requirements.

