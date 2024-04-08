provider "aws" {
  region = "us-east-1"
}

resource "aws_kinesis_stream" "event_stream" {
  name             = "event-stream"
  shard_count      = 2
}

resource "aws_iam_role" "kinesis_role" {
  name = "kinesis-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = {
        Service = "kinesis.amazonaws.com"
      }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "kinesis_policy" {
  name   = "kinesis-policy"
  policy = <<POLICY
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "kinesis:PutRecord",
          "kinesis:PutRecords"
        ],
        "Resource": "${aws_kinesis_stream.event_stream.arn}"
      }
    ]
  }
  POLICY
}

resource "aws_iam_role_policy_attachment" "kinesis_role_attachment" {
  role       = aws_iam_role.kinesis_role.name
  policy_arn = aws_iam_policy.kinesis_policy.arn
}

resource "aws_s3_bucket" "event_bucket" {
  bucket = "babbel-streaming-bucket"
  force_destroy = true
  # bucket_prefix = "processed_events"

  tags = {
    Name = "dev"
  }
}

resource "aws_s3_bucket_ownership_controls" "event_bucket" {
  bucket = aws_s3_bucket.event_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "event_bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.event_bucket]

  bucket = aws_s3_bucket.event_bucket.id
  acl    = "private"
}


