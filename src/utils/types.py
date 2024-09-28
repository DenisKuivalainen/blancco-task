from typing import TypedDict, List, Dict
from enum import Enum


class UploadedDevice(TypedDict):
    type: str
    state: str
    timestamp: str


class StatisticsDevice(TypedDict):
    id: str
    type: str
    state: str
    data: str


class ProcessedDevices(TypedDict):
    processed_devices: List[UploadedDevice]


class StatisticsType(Enum):
    type = "type"
    state = "state"
    date = "date"


DevicesStatisticsObject = Dict[str, int]


class StatisticRecord(TypedDict):
    type: str
    value: str
    count: int
