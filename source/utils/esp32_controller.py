import requests

from config.settings import ESP32_URL

def open_access():

    try:

        requests.get(
            f"{ESP32_URL}/open",
            timeout=2
        )

    except Exception as e:

        print("ESP32 ERROR:", e)

def deny_access():

    try:

        requests.get(
            f"{ESP32_URL}/deny",
            timeout=2
        )

    except Exception as e:

        print("ESP32 ERROR:", e)