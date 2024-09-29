import json
from utils.dynamodb_helpers import put_device
from utils.lambda_utils import format_response, error_hander
from utils.types import ProcessedDevices


def _handler(event, context):
    body: ProcessedDevices = json.loads(event["body"])
    processed_devices = body["processed_devices"]

    for device in processed_devices:
        put_device(device)

    return format_response(200, {"ok": True})


handler = error_hander(_handler)
