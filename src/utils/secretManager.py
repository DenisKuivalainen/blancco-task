import boto3

secrets_client = boto3.client("secretsmanager")


def getSecret(arn: str):
    secret = secrets_client.get_secret_value(SecretId=arn)
    return secret.get("SecretString")
