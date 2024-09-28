from utils.lambdaUtils import formatResponse, errorHandler
from utils.types import StatisticsType
from utils.dynamodbHelpers import getDeviceStatistics


def _handler(event, context):
    typeStatistics = getDeviceStatistics(StatisticsType.type)
    stateStatistics = getDeviceStatistics(StatisticsType.state)
    dateStatistics = getDeviceStatistics(StatisticsType.date)

    return formatResponse(
        200,
        {
            "ok": True,
            "data": {
                "type": typeStatistics,
                "state": stateStatistics,
                "date": dateStatistics,
            },
        },
    )


handler = errorHandler(_handler)
