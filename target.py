from dataclasses import dataclass

@dataclass
class Target:

    #YOLO tarafından tespit edilen tek bir nesnenin temsili

    #Class bilgileri
    class_id: int
    class_name: str
    confidence: float

    #Bounding box kordinatları
    x1:int
    y1:int
    x2:int
    y2:int

    #Merkez nokta
    center_x: int
    center_y:int

    #Bounding box boyutları (Alan, genişlik, yükseklik)
    area: int

    width: int
    height: int

    
    #Görüntü merkezine göre hata
    error_x: int
    error_y: int
    
    #Görüntü merkeiznee uzaklık
    distance: float