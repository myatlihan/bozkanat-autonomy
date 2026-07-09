from enum import Enum

from config import RED_SQUARE, BLUE_SQUARE

class MissionState(Enum):
    #Görev Durumları
    IDLE = 0            #Görev başlamadı.
    SEARCH = 1          #Hedef aranıyor                    
    TRACK = 2           #Hedef takip ediliyor.
    DROP = 3            #Yük bırakılıyor
    FINISHED = 4        #Görev tamamlandı.


class Mission:
    """
    Görev yöneticisi.

    Sorumlulukları:
    - Hedef sırasını belirlemek
    - Görev durumunu yönetmek
    - Kaç yük bırakıldığını takip etmek
    - Bir sonraki hedefe geçmek
    """


    def __init__(self):
        #Görev durumu
        self.state = MissionState.IDLE

        #Operatörün yük seçimi
        self.target_sequence = []

        #Şuan takip edilen hedef
        self.current_target_index = 0

        #Bırakılna yük sayısı
        self.drop_count = 0

        #Hedef bulundu mu ?
        self.target_detected = False

        #Tracker hedefi kilitledi mi?
        self.target_locked = False


    def select_payload_order(self, first_payload: str):
        '''
        İlk bırakılacak yükü belirler.

        red -> blue_square -> red_square
        blue -> red_square -> blue_square
        '''

        if first_payload.lower() == 'red':

            self.target_sequence = [
                BLUE_SQUARE,
                RED_SQUARE
            ]

        elif first_payload.lower == 'Blue':

            self.target_sequence = [
                RED_SQUARE,
                BLUE_SQUARE
            ]

        else: 
            raise ValueError('Geçersiz yük')
        
        self.state = MissionState.SEARCH


        def get_current_target(self):
            '''
            Şu anda aranacak hedef
            '''
            return self.target_sequence[self.current_target_index]

        def target_found(self):
            '''
            Hedef bulundu.
            '''
            self.target_detected = True
            self.state= MissionState.TRACK

        def target_lost(self):
            '''
            Hedef kaybedildi.
            '''
            self.target_detected = False
            self.target_locked = False
            self.state = MissionState.SEARCH

        def target_lock(self):
            '''
            Tracker hedefi başarıyla kilitledi
            '''
            self.target_locked = True

        def target_unlock(self):
            '''
            Kilit kaybedildi.
            '''
            self.target_locked = False
            self.state = MissionState.SEARCH

        def ready_to_drop(self) -> bool:
            '''
            Yük bırakmaya hazır mı ? 
            '''
            return self.target_detected and self.target_locked
        

        def payload_dropped(self):
            '''
            Servo yükü bıraktıktan sonra çağrılır.
            '''
            self.drop_count += 1
            self.current_target_index += 1

            self.target_detected = False
            self.target_locked = False

            if self.current_target_index >= len(self.target_sequence):
                self.state = MissionState.FINISHED
            else:
                self.state = MissionState.SEARCH

        def is_finished(self) -> bool:
            '''
            Görev tamamlandı mı ?
            '''
            return self.state == MissionState.FINISHED

        def set_state(self, state: MissionState):
            '''
            Görev durumunu değiştir.
            '''
            self.state = state
