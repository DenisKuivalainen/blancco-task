import json
from utils.dynamodbHelpers import updateDeviceStatistics
from utils.types import DevicesStatisticsObject, StatisticsType, StatisticsDevice
from typing import List


def updateStatisticsObject(dict: DevicesStatisticsObject, key: str):
    if key in dict:
        dict[key] = dict[key] + 1
    else:
        dict[key] = 1


def handler(event, context):
    devices: List[StatisticsDevice] = list(
        map(lambda record: json.loads(record["body"]), event["Records"])
    )

    typeStatistics: DevicesStatisticsObject = {}
    stateStatistics: DevicesStatisticsObject = {}
    dateStatistics: DevicesStatisticsObject = {}

    for device in devices:
        updateStatisticsObject(typeStatistics, device["type"])
        updateStatisticsObject(stateStatistics, device["state"])
        updateStatisticsObject(dateStatistics, device["date"])

    updateDeviceStatistics(typeStatistics, StatisticsType.type)
    updateDeviceStatistics(stateStatistics, StatisticsType.state)
    updateDeviceStatistics(dateStatistics, StatisticsType.date)
