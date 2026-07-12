from enum import Enum

from config import (
    RED_SQUARE,
    BLUE_SQUARE
)


class MissionState(Enum):
    """
    Görev durumları
    """

    IDLE = 0
    SEARCH = 1
    PAYLOAD = 2
    FINISHED = 3


class Mission:
    """
    Görev yöneticisi.

    Sorumlulukları

    - Görev sırasını belirlemek
    - Aktif hedefi belirlemek
    - Yük bırakıldıktan sonra sonraki hedefe geçmek
    - Görev durumunu yönetmek
    """

    def __init__(self):

        # Görev durumu
        self.current_state = MissionState.IDLE

        # Takip edilecek hedef sırası
        self.target_sequence = []

        # Aktif hedef indeksi
        self.current_index = 0

        # Bırakılan yük sayısı
        self.drop_count = 0

    def select_payload_order(
        self,
        first_payload: str
    ):
        """
        Operatörün seçimine göre hedef sırasını oluşturur.
        """

        if first_payload == "red":

            self.target_sequence = [
                BLUE_SQUARE,
                RED_SQUARE
            ]

        elif first_payload == "blue":

            self.target_sequence = [
                RED_SQUARE,
                BLUE_SQUARE
            ]

        else:

            raise ValueError(
                "Invalid payload selection."
            )

        self.current_state = MissionState.SEARCH

    def get_current_target(self):
        """
        Şu anda takip edilmesi gereken hedef.
        """

        if self.current_index >= len(
            self.target_sequence
        ):
            return None

        return self.target_sequence[
            self.current_index
        ]

    def payload_dropped(self):
        """
        Servo yükü bıraktıktan sonra çağrılır.
        """

        self.current_index += 1

        self.drop_count += 1

        if self.current_index >= len(
            self.target_sequence
        ):

            self.current_state = MissionState.FINISHED

        else:

            self.current_state = MissionState.SEARCH

    def is_finished(self) -> bool:
        """
        Görev tamamlandı mı?
        """

        return (
            self.current_state
            ==
            MissionState.FINISHED
        )

    def set_state(
        self,
        state: MissionState
    ):
        """
        Görev durumunu değiştir.
        """

        self.current_state = state

    def get_state(self):
        """
        Güncel görev durumu.
        """

        return self.current_state