import os
from utils.secretManager import getSecret


def handler(event, context):
    apiKeyArn = os.environ["API_KEY_SECRET_ARN"]
    apiKey = getSecret(apiKeyArn)

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
