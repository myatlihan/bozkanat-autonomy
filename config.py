'''
Project configuration
'''

#Camera
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

FRAME_CENTER_X = FRAME_WIDTH // 2
FRAME_CENTER_Y = FRAME_HEIGHT // 2


#YOLO
MODEL_PATH = 'models/bets.pt'
CONFIDENCE_THRESHOLD = 0.50
IMAGE_SIZE = 640


#Target Classes
BLUE_SQUARE = 'blue_square'
RED_SQUARE = 'red_square'

BLUE_HEXAGON = 'blue_hexagon'
RED_TRIANGLE = 'red_triangle'

ALL_TARGETS = [
    BLUE_SQUARE,
    RED_SQUARE,
    BLUE_HEXAGON,
    RED_TRIANGLE
]

MISSION_TARGETS = [
    BLUE_SQUARE,
    RED_SQUARE
]


#Tracker
CENTER_THRESHOLD = 20
LOCK_FRAME_COUNT = 5
LOST_FRAME_COUNT = 10



#Communication
#Pixhawk bağlantı portu
PORT = "/dev/ttyACM0"

#MAVLink haberleşme hızı
BAUDRATE = 57600

#Heartbeat bekleme süresi (saniye)
CONNECTION_TIMEOUT = 5
