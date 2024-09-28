import json
from utils.dynamodbHelpers import putDevice
from utils.lambdaUtils import formatResponse, errorHandler
from utils.types import ProcessedDevices


def _handler(event, context):
    body: ProcessedDevices = json.loads(event["body"])
    processedDevices = body["processed_devices"]

    for device in processedDevices:
        putDevice(device)

    return formatResponse(200, {"ok": True})


handler = errorHandler(_handler)
