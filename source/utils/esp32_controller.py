import requests

from utils.config import esp32_url

def open_access():

    try:

        requests.get(
            f"{esp32_url}/open",
            timeout=2
        )

    except Exception as e:

        print("ESP32 ERROR:", e)

def deny_access():

    try:

        requests.get(
            f"{esp32_url}/deny",
            timeout=2
        )

    except Exception as e:

        print("ESP32 ERROR:", e)