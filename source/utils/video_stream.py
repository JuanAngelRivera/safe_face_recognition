import cv2
import time
import numpy as np
import source.utils.config as config

_capture = None


def start_camera():
    global _capture
    
    if _capture is not None:
        try:
            _capture.release()
        except:
            pass
        _capture = None
    
    time.sleep(0.3)
    
    camera_source = config.camera_source
    if camera_source.isdigit():
        camera_source = int(camera_source)
    
    # Intentar con el backend del .env primero
    # Si falla, probar otros backends
    _capture = cv2.VideoCapture(camera_source, cv2.CAP_MSMF)
    
    if not _capture.isOpened():
        _capture = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
    
    if not _capture.isOpened():
        _capture = cv2.VideoCapture(camera_source)  # Default
    
    if _capture is not None and _capture.isOpened():
        _capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        _capture.set(cv2.CAP_PROP_FPS, 15)
    
    return _capture


def stop_camera():
    global _capture
    if _capture is not None:
        try:
            _capture.release()
        except:
            pass
        _capture = None


def get_frame():
    global _capture
    
    if _capture is None or not _capture.isOpened():
        start_camera()
        time.sleep(0.3)
    
    if _capture is not None and _capture.isOpened():
        for _ in range(2):
            _capture.grab()
        
        ret, frame = _capture.read()
        if ret and frame is not None:
            return frame
    
    return None


def generate_stream():
    start_camera()
    
    while True:
        frame = get_frame()
        
        if frame is None:
            time.sleep(0.2)
            continue
        
        frame = cv2.flip(frame, 1)
        
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 65])
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.05)