import json
from utils.dynamodb_helpers import update_device_statistics
from utils.types import DevicesStatisticsObject, StatisticsType, StatisticsDevice
from typing import List


def update_statistics_object(dict: DevicesStatisticsObject, key: str):
    if key in dict:
        dict[key] = dict[key] + 1
    else:
        dict[key] = 1


def handler(event, context):
    devices: List[StatisticsDevice] = list(
        map(lambda record: json.loads(record["body"]), event["Records"])
    )

    type_statistics: DevicesStatisticsObject = {}
    state_statistics: DevicesStatisticsObject = {}
    date_statistics: DevicesStatisticsObject = {}

    for device in devices:
        update_statistics_object(type_statistics, device["type"])
        update_statistics_object(state_statistics, device["state"])
        update_statistics_object(date_statistics, device["date"])

    update_device_statistics(type_statistics, StatisticsType.type)
    update_device_statistics(state_statistics, StatisticsType.state)
    update_device_statistics(date_statistics, StatisticsType.date)
