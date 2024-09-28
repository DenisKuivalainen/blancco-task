import random
import requests
import os
from datetime import datetime, timedelta


def generateDeviceData():
    types = ["laptop", "phone", "server"]
    states = ["erased", "erasure failed"]

    selectedType = random.choice(types)
    selectedState = random.choice(states)

    randomDate = datetime.now() - timedelta(random.randint(0, 30))
    timestamp = randomDate.strftime("%Y-%m-%dT%H:%M:%SZ")

    return {"type": selectedType, "state": selectedState, "timestamp": timestamp}


def generateDeviceDataArray():
    return [generateDeviceData() for _ in range(random.randint(4, 40))]


def main():
    url = os.environ["URL"] + "devices"
    data = {"processed_devices": generateDeviceDataArray()}
    headers = {"Authorization": os.environ["API_KEY"]}

    requests.post(url=url, json=data, headers=headers)


main()
