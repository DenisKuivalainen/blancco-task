from typing import List, Any
from utils.types import StatisticsDevice
import utils._sqs as sqs
import os


def transformDeviceRecords(records: List[Any]) -> List[StatisticsDevice]:
    return [
        {
            "id": record["dynamodb"]["NewImage"]["id"]["S"],
            "type": record["dynamodb"]["NewImage"]["type"]["S"].replace(" ", "_"),
            "state": record["dynamodb"]["NewImage"]["state"]["S"].replace(" ", "_"),
            "date": record["dynamodb"]["NewImage"]["timestamp"]["S"][:10],
        }
        for record in records
    ]


def handler(event, context):
    devices = transformDeviceRecords(event["Records"])

    sqs.sendBatch(messages=devices, url=os.getenv("QUEUE_URL"))
