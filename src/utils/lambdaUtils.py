import json


def formatResponse(status, body):
    return {"statusCode": status, "body": json.dumps(body)}


def errorHandler(fn):
    def inner(event, context):
        try:
            return fn(event, context)

        except Exception as e:
            return formatResponse(500, {"ok": False, "message": str(e)})

    return inner
