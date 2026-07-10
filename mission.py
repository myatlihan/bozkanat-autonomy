from enum import Enum
from config import (
    RED_SQUARE,
    BLUE_SQUARE,
    MISSION_TARGETS
)

class MissionState(Enum):
    '''
    Görev durumları
    '''
    IDLE = 0            #Görev başlamadı
    SEARCH = 1          #Hedef aranıyor
    TRACK = 2           #Hedef takip ediliyor
    PAYLOAD = 3         #Yük bırakılıyor
    FINISHED = 4        #Görev tamamlandı

class Mission:
    ''''
    Görev yöneticisi sınıfı
    Sorumluluklar:
        -Hedef sırasını belirlemek
        -Görev durumunu yönetmek
        -Kaç yük bırakıldığını takip etmek
        -Bir sonraki hedefe geçmek
    '''

    def __init__(self):

        #Görev durumu
        self.current_state = MissionState.IDLE
        
        #Operatörün yük seçimi (Aranacak alanın isimlerinin sırasıyla listesi)
        self.target_sequence = []

        #Şu an odaklanılan hedefin target_sequence içindeki indeksi
        self.current_index = 0

        #Bırakılan yük sayısı
        self.drop_count = 0

        #Hedef bulundu mu ?
        self.target_detected = False

        #Kamera hedefe tam olarak kilitlendi mi (merkezlendi mi)
        self.target_locked = False


    def select_payload_order(self, first_payload: str):
        """
        İlk bırakılacak yükün rengine göre tüm görev sırasını belirler.
        Örnek: 
        İlk yük 'red'  ise, önce mavi alan bulunmmalı, sonra kırmızı.
        """
        if first_payload == 'red':
            self.target_sequence = [
                BLUE_SQUARE,
                RED_SQUARE
            ]

        elif first_payload == 'blue':
            self.target_sequence = [
                RED_SQUARE,
                BLUE_SQUARE
            ]

        else:
            raise ValueError('Geçersiz yük')
        
        self.current_state = MissionState.SEARCH


    def get_current_target(self):
        '''
        Şu anda aranacak hedef
        '''

        if (
            not self.target_sequence #1. Durum: Hedef listesi bomboş mu?
            or self.current_index >= len(self.target_sequence)): #2. Durum: Sıra bitti mi?
            return None 
        
        return self.target_sequence[self.current_index]
    

    def target_found(self):
        '''
        Hedef bulundu
        '''

        self.target_detected = True
        self.current_state = MissionState.TRACK


    def target_lost(self):
        '''
        Hedef kaybedildi.
        '''

        self.target_detected = False
        self.target_locked = False
        self.current_state = MissionState.SEARCH


    def target_unlock(self):
        '''
        Kilit kaybedildi
        '''

        self.target_locked = False
        self.current_state = MissionState.SEARCH


    def ready_to_drop(self) -> bool:
        '''
        Yük bırakılmaya hazır mı ?
        '''

        return self.target_detected and self.target_locked
    

    def payload_dropped(self):
        '''
        Yük bırakma.
        ! Servo yükü bıraktıktan sonra çağrılır !
        '''

        self.current_index += 1 
        self.drop_count +=1

        # Yeni hedef için kilitleri sıfırlama
        self.target_detected =False
        self.target_locked = False

        # Tüm hedefler bitti mi ?
        if self.current_index >= len(self.target_sequence):
            self.current_state = MissionState.FINISHED
        else:
            self.current_state = MissionState.SEARCH


    def is_finished(self) -> bool:
        '''
        Görev tamamlandı mı ? 
        '''

        return self.current_state == MissionState.FINISHED
    

    def set_state(self, state: MissionState):
        '''
        Görev durumunu dışarıdan değiştir.
        '''

        if isinstance(state, MissionState):
            self.current_state = state
        else:
            raise TypeError("State parametresi Mission state Enum'ı olmal")