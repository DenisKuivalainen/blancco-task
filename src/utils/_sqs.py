import boto3
from typing import List, Any
import json
import uuid

sqs = boto3.client("sqs")


def sendBatch(url: str, messages: List[Any]):
    entries = [
        {
            "Id": str(uuid.uuid4()),
            "MessageBody": json.dumps(message),
            "MessageGroupId": "blancco",
        }
        for message in messages
    ]

    sqs.send_message_batch(QueueUrl=url, Entries=entries)
