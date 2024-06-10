from io import BytesIO
from picamera2 import Picamera2, configuration
import numpy as np
from PIL import Image
import cv2


class Camera():
    _compression: int = 50
    
    
    def __init__(self):
        self.configuration: configuration = None
        self.camera: Picamera2 = self._create_camera_object()
        self.camera.configure(self._create_configuration())
        self.camera.start()
    
    
    def get_jpeg_bytes(self) -> bytes:
        byte_io = BytesIO()
        array = self._get_frame()
        print("array size: ", array[: ,: , 0])
        array[:, :, 0] = array[:, :, 0]/1.5
        Image.fromarray(array[:, :, :3]).save(byte_io, format='JPEG')
        
        return byte_io.getvalue()
        
    
    def _get_frame(self) -> np.ndarray:
        return self.camera.capture_array()
    
    
    def _create_configuration(self) -> dict:
        if self.camera:
            
            mode = self.camera.sensor_modes[1]
            
            self.camera.white_balance_mode = 'manual'
			
            config = self.camera.create_video_configuration(
                sensor={'output_size': mode['size'], 
                        'bit_depth': mode['bit_depth']},
				controls={"AwbEnable": False,
						 "ColourGains": (0.95, 1.0),
                         "FrameDurationLimits": (33333, 33333)},
                buffer_count=1
				#white_balance=(0.95, 1.2)
                )
            return config
        else:
            raise ReferenceError("Can't configure no existing camera.")
    
    
    def _create_camera_object(self) -> Picamera2:
        try:
            camera = Picamera2(camera_num=0)
        except RuntimeError as e:
            print(f"Could not create Picamera object. Exception: {e}")
            return None
        return camera
    
    
    def set_compression(self, quality: int):
        self._compression = int(np.clip(quality, 5, 100))
    
    
    def take_photo(self):
    """ Takes a photo and saves it in archiwization purpose
    """
        raise NotImplementedError()
    