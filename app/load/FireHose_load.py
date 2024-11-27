import boto3
import os
import json

# Creating session variables
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SESSION_TOKEN = os.environ["AWS_SESSION_TOKEN"]
AWS_REGION = os.environ["AWS_REGION"]

# Accessing session
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_REGION,
)

# Test it on a service
firehose = session.resource("firehose")


# Function to send data to firehose
def send_data(price, coleta):
    firehose.put_record(
        DeliveryStreamName="",
        Record={"Data": json.dumps({"price": price, "coleta": coleta})},
    )
