from io import BytesIO
from picamera2 import Picamera2, configuration
from time import sleep, time
import numpy as np
from libcamera import Transform
from PIL import Image

class Camera():
    _last_frame_time: int = time()
    _frame_rate: int = 20
    _compression: int = 50
    
    # temp
    __last_frame_time = time()
    
    def __init__(self):
        self.configuration: configuration = None
        self.camera = self._create_camera_object()
        self.camera.configure(self._create_configuration())
        self.camera.start()
    
    
    def get_jpeg_bytes(self) -> bytes:
        start = time()
        pil_image = Image.fromarray(self._get_frame()[:, :, :3])
        take_pic_end = time()
        print("take picture time: ", take_pic_end - start)
        image_bytes = BytesIO()
        pil_image.save(image_bytes, format='jpeg', quality=self._compression)
        bytes = image_bytes.getvalue()
        end = time()
        print("encode time: ", end - take_pic_end)
        print("send time: ", start - self.__last_frame_time)
        print(f"\nfull time: ", end - self.__last_frame_time)
        self.__last_frame_time = start
        
        
        return bytes
        
    
    def _get_frame(self) -> np.ndarray:
        array = self.camera.capture_array()
        return array
    
    
    def _create_configuration(self) -> dict:
        if self.camera:
            mode = self.camera.sensor_modes[1]
            
            config = self.camera.create_video_configuration(
                sensor={'output_size': mode['size'], 
                        'bit_depth': mode['bit_depth']},
                buffer_count=1,
                # Temporary
                transform=Transform(vflip=1)
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
        raise NotImplementedError()