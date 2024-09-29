import random
import requests
import os
from datetime import datetime, timedelta


def generate_device_data():
    types = ["laptop", "phone", "server"]
    states = ["erased", "erasure failed"]

    selected_type = random.choice(types)
    selected_state = random.choice(states)

    random_date = datetime.now() - timedelta(random.randint(0, 30))
    timestamp = random_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    return {"type": selected_type, "state": selected_state, "timestamp": timestamp}


def generate_device_data_array():
    return [generate_device_data() for _ in range(random.randint(4, 40))]


def main():
    url = os.environ["URL"] + "devices"
    data = {"processed_devices": generate_device_data_array()}
    headers = {"Authorization": os.environ["API_KEY"]}

    requests.post(url=url, json=data, headers=headers)


main()
