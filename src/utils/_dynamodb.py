import boto3
from typing import Dict, Any, Optional

dynamodb = boto3.resource("dynamodb")


def query(tableName: str, keyConditionExpression) -> Optional[Dict[str, Any]]:
    response = dynamodb.Table(tableName).query(
        KeyConditionExpression=keyConditionExpression
    )
    return response.get("Items", [])


def put(tableName: str, item: Dict[str, Any]):
    dynamodb.Table(tableName).put_item(Item=item)


def update(
    tableName: str,
    key: Dict[str, Any],
    updateExpression: str,
    expressionAttributeNames: Dict[str, str],
    expressionAttributeValues: Dict[str, Any],
):
    dynamodb.Table(tableName).update_item(
        Key=key,
        UpdateExpression=updateExpression,
        ExpressionAttributeNames=expressionAttributeNames,
        ExpressionAttributeValues=expressionAttributeValues,
    )


# TODO: Add other db acess methods here
