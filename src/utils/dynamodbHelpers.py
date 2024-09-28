import os
import utils._dynamodb as dynamodb
import uuid
from utils.types import (
    UploadedDevice,
    DevicesStatisticsObject,
    StatisticsType,
    StatisticRecord,
    DevicesStatisticsObject,
    List,
)
from typing import Optional, Dict
import boto3


def putDevice(input: UploadedDevice):
    dynamodb.put(
        tableName=os.getenv("DEVICES_TABLE"), item={**input, "id": str(uuid.uuid4())}
    )


def updateDeviceStatistics(
    statisticsObject: DevicesStatisticsObject, type: StatisticsType
):
    statisticsTableName = os.getenv("STATISTICS_TABLE")

    statistics = [[k, v] for k, v in statisticsObject.items()]

    for [value, n] in statistics:
        statisticsInDb: Optional[StatisticRecord] = dynamodb.query(
            tableName=statisticsTableName,
            keyConditionExpression=boto3.dynamodb.conditions.Key("type").eq(type.value)
            & boto3.dynamodb.conditions.Key("value").eq(value),
        )
        statisticInDb = statisticsInDb[0] if statisticsInDb else None

        if statisticInDb is None:
            dynamodb.put(
                tableName=statisticsTableName,
                item={"type": type.value, "value": value, "count": n},
            )
        else:
            dynamodb.update(
                key={"type": type.value, "value": value},
                updateExpression="SET #count = :count",
                expressionAttributeNames={"#count": "count"},
                expressionAttributeValues={":count": statisticInDb["count"] + n},
                tableName=statisticsTableName,
            )


def getDeviceStatistics(type: StatisticsType) -> DevicesStatisticsObject:
    statisticsInDb: List[StatisticRecord] = dynamodb.query(
        tableName=os.getenv("STATISTICS_TABLE"),
        keyConditionExpression=boto3.dynamodb.conditions.Key("type").eq(type.value),
    )

    return {statistic["value"]: int(statistic["count"]) for statistic in statisticsInDb}
