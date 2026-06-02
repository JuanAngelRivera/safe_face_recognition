# source/utils/video_stream.py
import cv2
import threading
import time
import source.utils.config as config

_capture = None
_lock = threading.Lock()
_frame = None
_active = False


def start_camera():
    """Inicia la cámara una sola vez"""
    global _capture, _active, _frame
    
    if _capture is not None and _capture.isOpened():
        return _capture
    
    camera_source = config.camera_source
    if camera_source.isdigit():
        camera_source = int(camera_source)
    
    _capture = cv2.VideoCapture(camera_source)
    _active = True
    
    def capture_loop():
        global _frame
        while _active:
            if _capture is not None and _capture.isOpened():
                ret, frame = _capture.read()
                with _lock:
                    _frame = frame.copy() if ret else None
            time.sleep(0.03)
    
    thread = threading.Thread(target=capture_loop, daemon=True)
    thread.start()
    
    return _capture


def stop_camera():
    """Detiene la cámara"""
    global _active, _capture
    _active = False
    if _capture:
        _capture.release()
        _capture = None


def get_frame():
    """Obtiene frame actual"""
    global _frame
    with _lock:
        if _frame is None:
            return None
        return _frame.copy()


def generate_stream():
    """Generador para el stream MJPEG"""
    start_camera()
    
    while _active:
        frame = get_frame()
        
        if frame is None:
            time.sleep(0.1)
            continue
        
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')