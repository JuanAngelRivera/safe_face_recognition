import os
from dotenv import load_dotenv

load_dotenv()

camera_source = os.getenv('CAMERA_SOURCE')
face_match_threshold = os.getenv('FACE_MATCH_THRESHOLD')
esp32_url = os.getenv('ESP32_URL')