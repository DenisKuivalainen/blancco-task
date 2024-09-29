import json


def format_response(status, body):
    return {"statusCode": status, "body": json.dumps(body)}


def error_hander(fn):
    def inner(event, context):
        try:
            return fn(event, context)

        except Exception as e:
            return format_response(500, {"ok": False, "message": str(e)})

    return inner
