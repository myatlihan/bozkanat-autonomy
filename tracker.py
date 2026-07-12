"""
tracker.py

Target Tracker Module

Bu modülün sorumlulukları:

- Mission tarafından belirlenen hedefi takip etmek
- Aynı sınıftaki hedefler arasından en uygununu seçmek
- Hedefin görüntü merkezinde olup olmadığını kontrol etmek
- Kilitlenme durumunu yönetmek
- Kısa süreli hedef kayıplarını yönetmek
"""

from config import (
    CENTER_THRESHOLD,
    LOCK_FRAME_COUNT,
    LOST_FRAME_COUNT
)

from target import Target


class Tracker:
    """
    Hedef takip sınıfı.

    Bu sınıf yalnızca hedef takibinden sorumludur.
    """

    def __init__(self):
        """
        Tracker başlangıç ayarları.
        """

        # Takip edilecek hedef sınıfı
        self.target_name = None

        # Güncel takip edilen hedef
        self.current_target: Target | None = None

        # Kilit durumu
        self.locked = False

        # Arka arkaya merkezde görülen frame sayısı
        self.lock_counter = 0

        # Arka arkaya kaybolan frame sayısı
        self.lost_counter = 0

    def set_target(self, target_name: str):
        """
        Takip edilecek hedef sınıfını belirler.
        """

        self.target_name = target_name

        # Yeni hedef seçildiğinde tracker sıfırlanır
        self.reset()

    def update(
        self,
        targets: list[Target]
    ) -> Target | None:
        """
        Her framede tracker'ı günceller.
        """

        # Takip edilecek hedef belirlenmemiş
        if self.target_name is None:
            return None

        target = self._find_best_target(targets)

        # Hedef bulunamadı
        if target is None:

            self.lost_counter += 1

            if self.lost_counter >= LOST_FRAME_COUNT:
                self.reset()

            return self.current_target

        # Hedef tekrar bulundu
        self.current_target = target

        self.lost_counter = 0

        # Merkez kontrolü
        if self._is_centered(target):

            self.lock_counter += 1

        else:

            self.lock_counter = 0

        # Kilit durumu
        self.locked = (
            self.lock_counter >= LOCK_FRAME_COUNT
        )

        return self.current_target

    def _find_best_target(
        self,
        targets: list[Target]
    ) -> Target | None:
        """
        Aynı sınıftaki hedefler arasından
        merkeze en yakın olanı seçer.
        """

        candidates = []

        for target in targets:

            if target.class_name == self.target_name:
                candidates.append(target)

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda target: target.distance
        )

    def _is_centered(
        self,
        target: Target
    ) -> bool:
        """
        Hedef merkez toleransı içerisinde mi?
        """

        return (
            abs(target.error_x) <= CENTER_THRESHOLD
            and
            abs(target.error_y) <= CENTER_THRESHOLD
        )

    def is_locked(self) -> bool:
        """
        Hedef kilitlendi mi?
        """

        return self.locked

    def get_target(self) -> Target | None:
        """
        Güncel takip edilen hedef.
        """

        return self.current_target

    def reset(self):
        """
        Tracker'ı başlangıç durumuna döndürür.
        """

        self.current_target = None

        self.locked = False

        self.lock_counter = 0

        self.lost_counter = 0