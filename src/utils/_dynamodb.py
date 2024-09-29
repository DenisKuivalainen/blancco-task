import boto3
from typing import Dict, Any, Optional

dynamodb = boto3.resource("dynamodb")


def query(table_name: str, key_condition_expression) -> Optional[Dict[str, Any]]:
    response = dynamodb.Table(table_name).query(
        KeyConditionExpression=key_condition_expression
    )
    return response.get("Items", [])


def put(table_name: str, item: Dict[str, Any]):
    dynamodb.Table(table_name).put_item(Item=item)


def update(
    table_name: str,
    key: Dict[str, Any],
    update_expression: str,
    expression_attribute_names: Dict[str, str],
    expression_attribute_values: Dict[str, Any],
):
    dynamodb.Table(table_name).update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
    )


# TODO: Add other db acess methods here
