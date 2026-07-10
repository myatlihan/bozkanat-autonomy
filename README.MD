# Sabit Kanat İHA Otonom Nesne Tespit ve Hedef Takip Sistemi (Geliştirme Aşamasında)

Bu proje; Sabit Kanat kategorisindeki bir İHA (İnsansız Hava Aracı) için geliştirilmekte olan, gerçek zamanlı yapay zeka tabanlı nesne tespit, otonom karar/görev mekanizması (State Machine) mimarisidir. 

> Bu proje henüz **aktif geliştirme aşamasındadır**. Şu anki sürümde kamera akışı ve yapay zeka mantığı Raspberry Pi üzerinde koşturulmakta, uçuş kontrol kartı (Pixhawk) ve fiziksel servo motor tetiklemeleri terminal üzerinde simüle edilerek test edilmektedir.


## Sabit Kanat Konsepti ve Görev Mantığı
Sabit kanatlı İHA'lar, döner kanatlı (multirotor) platformlar gibi havada asılı (**loitering/hover**) kalamazlar. Bu durum, hedef takip ve yük bırakma sisteminin çok daha hızlı ve kararlı reflekslere sahip olmasını zorunlu kılar. 

Sistem; yüksek hızda seyreden uçağın kamerasından alınan görüntüleri gerçek zamanlı olarak YOLO modeliyle işler, operatörün belirlediği görev senaryosuna göre hedefleri süzerek en doğru anlık kilitlenme açısını hesaplar.


## Modüler Proje Yapısı

Sistem, yazılım dünyasındaki **Sorumlulukların Ayrılması (Single Responsibility)** prensibine uygun olarak tamamen modüler tasarlanmıştır:

*   `config.py`: Çözünürlük, model yolları, güven eşikleri gibi tüm sistem sabitleri.
*   `camera.py`: Raspberry Pi'nin yerel `Picamera2` arayüzünü kararlı bir şekilde sarmalayan kamera sınıfı.
*   `target.py`: YOLO çıktılarının dönüştürüldüğü, merkeze uzaklık ve piksel hatalarını tutan temiz bir `@dataclass` veri yapısı.
*   `detector.py`: YOLO modelini koşturan ve ham matris çıktılarını `Target` nesnelerine dönüştüren dedektör sınıfı.
*   `mission.py`: İHA'nın görev reflekslerini (`SEARCH`, `TRACK`, `PAYLOAD`, `FINISHED`) yöneten ana Durum Makinesi.
*   `test_terminal.py`: Grafik arayüz yükü yaratmadan, SSH üzerinden sistem kararlılığını izlemeyi sağlayan canlı telemetri ve simülasyon ekranı.



## Durum Makinesi (State Machine) İşleyişi

Sistem, operatörün ilk mühimmat/yük rengi seçimini yapmasıyla (`select_payload_order`) tetiklenir:

1.  **SEARCH (Arama):** Sabit kanat belirlenen rota hattında uçarken kamera aktifleşir ve ilk hedef olan `BLUE_SQUARE` aranır.
2.  **TRACK (Takip):** Hedef kadraja girdiği an durum `TRACK` moduna geçer. Hedef merkezinin, ekran merkezine (crosshair) olan piksel hataları ($error_x, error_y$) hesaplanır.
3.  **LOCK (Kilitlenme):** Uçağın süzülüş açısı ve hızı göz önüne alınarak, hedef ekran merkezinde 15 kare boyunca kararlı şekilde kalırsa `target_locked = True` olur.
4.  **PAYLOAD (Yük Bırakma):** Kilit tamamlandığında servo mekanizması tetiklenir, yük bırakılır ve terminale simülasyon uyarısı düşer.
5.  **NEXT TARGET (Sonraki Hedef):** İndeks otomatik artar, kilitler sıfırlanır ve sistem ikinci hedef olan `RED_SQUARE` için tekrar **SEARCH** moduna döner.



## Mevcut Durum ve Yol Haritası

### Tamamlanan Modüller (Masaüstü/Laboratuvar Testleri Başarılı)
- Raspberry Pi `Picamera2` Entegrasyonu
- YOLO Tabanlı Nesne Tespit ve Veri Dönüştürücü Sınıfı
- Görev Yöneticisi ve Durum Makinesi Tasarımı
- SSH/Terminal Tabanlı Canlı Telemetri ve Karar Simülasyon Yazılımı

### Geliştirilmekte Olan Modüller (Sıradaki Adımlar)
- [ ] **Tracker Modülü:** Kadraja birden fazla nesne girdiğinde, sabit kanat mekaniğine en uygun (merkeze en yakın veya alanı en büyük) ana hedefi seçme filtresi.
- [ ] **Pixhawk/Mavlink Haberleşmesi:** `PyMAVLink` kütüphanesi kullanılarak Pixhawk uçuş kontrol kartına `GUIDED` modda otonom yönelim/hız komutları enjekte edilmesi.
- [ ] **Fiziksel Servo Entegrasyonu:** Hedefe kilitlenme doğrulandığında, mühimmat bırakma mekanizmasını tetikleyecek PWM sinyal yapısının kurulması.



## Çalıştırma (Simülasyon Modu)

Sistemi grafik arayüz yükü olmadan, tamamen terminal tabanlı bir telemetri ekranı üzerinden simüle etmek için:

```bash
pip install numpy ultralytics opencv-python
python3 test_terminal.py