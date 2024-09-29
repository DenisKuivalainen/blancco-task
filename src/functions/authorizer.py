import os
from utils.secrets_manager import get_secret


def handler(event, context):
    apiKeyArn = os.environ["API_KEY_SECRET_ARN"]
    apiKey = get_secret(apiKeyArn)

    headers = event.get("headers", {})

    return {
        "principalId": "apigateway.amazonaws.com",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": (
                        "Allow" if headers["Authorization"] == apiKey else "Deny"
                    ),
                    "Resource": event["methodArn"],
                }
            ],
        },
    }
