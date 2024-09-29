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


def put_device(input: UploadedDevice):
    dynamodb.put(
        tableName=os.getenv("DEVICES_TABLE"), item={**input, "id": str(uuid.uuid4())}
    )


def update_device_statistics(
    statistics_object: DevicesStatisticsObject, type: StatisticsType
):
    statistics_table_name = os.getenv("STATISTICS_TABLE")

    statistics = [[k, v] for k, v in statistics_object.items()]

    for [value, n] in statistics:
        statistics_in_db: Optional[StatisticRecord] = dynamodb.query(
            tableName=statistics_table_name,
            keyConditionExpression=boto3.dynamodb.conditions.Key("type").eq(type.value)
            & boto3.dynamodb.conditions.Key("value").eq(value),
        )
        statisticInDb = statistics_in_db[0] if statistics_in_db else None

        if statisticInDb is None:
            dynamodb.put(
                tableName=statistics_table_name,
                item={"type": type.value, "value": value, "count": n},
            )
        else:
            dynamodb.update(
                key={"type": type.value, "value": value},
                update_expression="SET #count = :count",
                expression_attribute_names={"#count": "count"},
                expression_attribute_values={":count": statisticInDb["count"] + n},
                tableName=statistics_table_name,
            )


def get_device_statistics(type: StatisticsType) -> DevicesStatisticsObject:
    statistics_in_db: List[StatisticRecord] = dynamodb.query(
        tableName=os.getenv("STATISTICS_TABLE"),
        keyConditionExpression=boto3.dynamodb.conditions.Key("type").eq(type.value),
    )

    return {
        statistic["value"]: int(statistic["count"]) for statistic in statistics_in_db
    }
