import math

from ultralytics import YOLO

from config import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    FRAME_WIDTH,
    FRAME_HEIGHT
)

from target import Target


class Detector:
    """
    YOLO tabanlı nesne tespit sınıfı.

    Sorumlulukları:
    - YOLO modelini yüklemek
    - Görüntü üzerinde tahmin yapmak
    - Tahminleri Target nesnelerine dönüştürmek
    """

    def __init__(self):

        # Eğitilmiş YOLO modelini yükle
        self.model = YOLO(MODEL_PATH)

        # Görüntünün merkez koordinatları
        self.frame_center_x = FRAME_WIDTH // 2
        self.frame_center_y = FRAME_HEIGHT // 2

    def detect(self, frame) -> list[Target]:
        """
        Görüntü üzerinde nesne tespiti yapar.

        Parametre:
            frame : Kameradan alınan görüntü

        Döndürür:
            list[Target] : Tespit edilen hedefler
        """

        # YOLO tahmini
        results = self.model.predict(
            source=frame,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        targets = []

        # Her tespit edilen nesne için Target oluştur
        for box in results[0].boxes:
            target = self._create_target(box)
            targets.append(target)

        return targets

    def _create_target(self, box) -> Target:
        """
        Tek bir YOLO tespitinden Target nesnesi oluşturur.
        """

        # Sınıf bilgileri
        class_id = int(box.cls[0])
        class_name = self.model.names[class_id]

        # Güven skoru
        confidence = float(box.conf[0])

        # Bounding Box koordinatları
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # box boyutları
        width = x2 - x1
        height = y2 - y1

        # Kutunun merkez noktası
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Alan hesabı
        area = width * height

        # Görüntü merkezine göre hata
        error_x = center_x - self.frame_center_x
        error_y = center_y - self.frame_center_y

        # Görüntü merkezine uzaklık
        distance = math.sqrt(error_x ** 2 + error_y ** 2)

        # Target nesnesini oluştur
        return Target(
            class_id=class_id,
            class_name=class_name,
            confidence=confidence,

            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,

            width=width,
            height=height,
            area=area,

            center_x=center_x,
            center_y=center_y,

            error_x=error_x,
            error_y=error_y,

            distance=distance
        )