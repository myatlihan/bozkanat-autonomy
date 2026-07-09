from picamera2 import Picamera2
from config import FRAME_WIDTH, FRAME_HEIGHT
import numpy as np


class Camera:
    
    """
    Raspberry Pi Camera arayüzü.

    Sorumlulukları:
        - Kamerayı başlatmak
        - Frame almak
        - Kamerayı durdurmak
    """

    def __init__(self,
                 width=FRAME_WIDTH,
                 height=FRAME_HEIGHT):

        self.width = width
        self.height = height

        self.camera = Picamera2()

        config = self.camera.create_preview_configuration(
            main={
                "size": (self.width, self.height),
                "format": "RGB888"
            }
        )

        self.camera.configure(config)

    def start(self) -> None:
        self.camera.start()

    def read(self) -> np.ndarray:
        return self.camera.capture_array()

    def stop(self) ->None:
        self.camera.stop()