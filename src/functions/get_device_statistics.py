from utils.lambda_utils import format_response, error_hander
from utils.types import StatisticsType
from utils.dynamodb_helpers import get_device_statistics


def _handler(event, context):
    type_statistics = get_device_statistics(StatisticsType.type)
    state_statistics = get_device_statistics(StatisticsType.state)
    date_statistics = get_device_statistics(StatisticsType.date)

    return format_response(
        200,
        {
            "ok": True,
            "data": {
                "type": type_statistics,
                "state": state_statistics,
                "date": date_statistics,
            },
        },
    )


handler = error_hander(_handler)
