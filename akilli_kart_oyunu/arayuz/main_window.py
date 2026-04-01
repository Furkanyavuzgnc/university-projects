from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QApplication
from veri.veri_okuyucu import VeriOkuyucu
from oyun.oyun_yonetici import OyunYonetici


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Akıllı Kart Oyunu")
        self.setGeometry(200, 200, 550, 650)

        self.layout = QVBoxLayout()

        self.skor_label = QLabel()
        self.skor_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 8px;")
        self.layout.addWidget(self.skor_label)

        self.label = QLabel()
        self.label.setStyleSheet("font-size: 15px; padding: 10px;")
        self.layout.addWidget(self.label)

        self.kart_layout = QVBoxLayout()
        self.layout.addLayout(self.kart_layout)

        self.devam_btn = QPushButton("Sonraki Tur")
        self.devam_btn.clicked.connect(self.sonraki_tur)
        self.devam_btn.setVisible(False)
        self.devam_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        self.layout.addWidget(self.devam_btn)

        self.restart_btn = QPushButton("🔁 Yeniden Oyna")
        self.restart_btn.clicked.connect(self.yeniden_baslat)
        self.restart_btn.setVisible(False)
        self.restart_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        self.layout.addWidget(self.restart_btn)

        self.cikis_btn = QPushButton("❌ Oyunu Bitir")
        self.cikis_btn.clicked.connect(self.cikis)
        self.cikis_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        self.layout.addWidget(self.cikis_btn)

        self.setLayout(self.layout)

        self.butonlar = []
        self.oyunu_baslat()

    # -------------------------------------------------
    # OYUN BAŞLAT
    # -------------------------------------------------
    def oyunu_baslat(self):
        kartlar = VeriOkuyucu.oku("veri/sporcular.txt")
        self.oyun = OyunYonetici(kartlar)
        self.oyun.kartlari_dagit()
        self.oyun.tur = 0

        self.butonsuz_temizle()

        self.devam_btn.setVisible(False)
        self.restart_btn.setVisible(False)

        self.skor_guncelle()
        self.kartlari_goster()

    # -------------------------------------------------
    # YARDIMCI
    # -------------------------------------------------
    def butonsuz_temizle(self):
        for btn in self.butonlar:
            self.kart_layout.removeWidget(btn)
            btn.deleteLater()
        self.butonlar = []

    def renk_getir(self, brans):
        if brans == "futbol":
            return """
                QPushButton {
                    background-color: #b9f6ca;
                    border: 2px solid #2e7d32;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #8be9a8;
                }
            """
        elif brans == "basketbol":
            return """
                QPushButton {
                    background-color: #ffd180;
                    border: 2px solid #ef6c00;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ffb74d;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #81d4fa;
                    border: 2px solid #0277bd;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4fc3f7;
                }
            """

    def skor_guncelle(self):
        self.skor_label.setText(
            f"Skor: Kullanıcı {self.oyun.skor_kullanici} - {self.oyun.skor_bilgisayar} Bilgisayar"
        )

    # -------------------------------------------------
    # OYUN BİTİŞ
    # -------------------------------------------------
    def oyun_bitti_mi(self):
        return (not self.oyun.kullanici_kartlar) and (not self.oyun.bilgisayar_kartlar)

    def oyun_bitti_ekrani(self):
        self.butonsuz_temizle()

        if self.oyun.skor_kullanici > self.oyun.skor_bilgisayar:
            sonuc = "🎉 Oyunu Kazandın!"
        elif self.oyun.skor_bilgisayar > self.oyun.skor_kullanici:
            sonuc = "💻 Bilgisayar Kazandı!"
        else:
            sonuc = "🤝 Oyun Berabere Bitti!"

        self.label.setText(
            "OYUN BİTTİ\n\n"
            f"{sonuc}\n\n"
            f"Final Skoru:\n"
            f"Kullanıcı: {self.oyun.skor_kullanici}\n"
            f"Bilgisayar: {self.oyun.skor_bilgisayar}"
        )

        self.devam_btn.setVisible(False)
        self.restart_btn.setVisible(True)

    # -------------------------------------------------
    # KARTLARI GÖSTER
    # -------------------------------------------------
    def kartlari_goster(self):
        if self.oyun_bitti_mi():
            self.oyun_bitti_ekrani()
            return

        self.butonsuz_temizle()

        brans = self.oyun.tur_sirasi[self.oyun.tur % 3]
        self.label.setText(f"Sıradaki Branş: {brans.upper()}\nLütfen bir kart seç.")

        uygun_kartlar = [k for k in self.oyun.kullanici_kartlar if k.brans == brans]
        uygun_bilgisayar = [k for k in self.oyun.bilgisayar_kartlar if k.brans == brans]

        # Kullanıcıda kart yoksa
        if not uygun_kartlar:
            # Bilgisayarda da yoksa tur atla
            if not uygun_bilgisayar:
                self.label.setText(
                    f"Sıradaki Branş: {brans.upper()}\n"
                    "Bu branşta iki tarafta da kart yok. Tur otomatik atlandı."
                )
            else:
                self.label.setText(
                    f"Sıradaki Branş: {brans.upper()}\n"
                    "Bu branşta kartın yok. Bilgisayar hükmen kazandı."
                )
                self.oyun.skor_bilgisayar += 8

                # Bilgisayarın o branştan bir kartını da oyundan çıkaralım
                # hükmen tur gerçekten oynanmış sayılsın
                bilgisayar_karti = uygun_bilgisayar[0]
                if bilgisayar_karti in self.oyun.bilgisayar_kartlar:
                    self.oyun.bilgisayar_kartlar.remove(bilgisayar_karti)

                self.skor_guncelle()

            self.devam_btn.setVisible(True)
            self.restart_btn.setVisible(False)
            return

        for kart in uygun_kartlar:
            btn = QPushButton(f"{kart.ad} | Enerji: {kart.enerji} | Seviye: {kart.seviye}")
            btn.setStyleSheet(self.renk_getir(kart.brans))
            btn.clicked.connect(lambda checked, k=kart: self.kart_sec(k))
            self.kart_layout.addWidget(btn)
            self.butonlar.append(btn)

    # -------------------------------------------------
    # KART SEÇ
    # -------------------------------------------------
    def kart_sec(self, kart):
        brans = self.oyun.tur_sirasi[self.oyun.tur % 3]
        ozellik = self.oyun.ozellik_sec(brans)

        b_kart = self.oyun.kart_sec_bilgisayar(brans, ozellik)

        # Bilgisayarın bu branşta kartı yoksa kullanıcı hükmen kazanır
        if b_kart is None:
            self.oyun.skor_kullanici += 8

            if kart in self.oyun.kullanici_kartlar:
                self.oyun.kullanici_kartlar.remove(kart)

            self.label.setText(
                f"Sıradaki Branş: {brans.upper()}\n"
                f"Seçtiğin Kart: {kart.ad}\n\n"
                "🎉 Sen hükmen kazandın!"
            )
            self.skor_guncelle()

            self.butonsuz_temizle()

            if self.oyun_bitti_mi():
                self.oyun_bitti_ekrani()
                return

            self.devam_btn.setVisible(True)
            self.restart_btn.setVisible(False)
            return

        # Kullanıcının seçtiği kartı elinden çıkar
        if kart in self.oyun.kullanici_kartlar:
            self.oyun.kullanici_kartlar.remove(kart)

        k_puan = kart.performans_hesapla(ozellik)
        b_puan = b_kart.performans_hesapla(ozellik)

        if k_puan > b_puan:
            self.oyun.skor_kullanici += 10
            sonuc = "🎉 Kazandın!"
        elif b_puan > k_puan:
            self.oyun.skor_bilgisayar += 10
            sonuc = "❌ Kaybettin!"
        else:
            sonuc = "🤝 Berabere!"

        self.label.setText(
            f"Branş: {brans.upper()}\n"
            f"Özellik: {ozellik}\n\n"
            f"Senin Kartın: {kart.ad} | Puan: {k_puan}\n"
            f"Bilgisayar Kartı: {b_kart.ad} | Puan: {b_puan}\n\n"
            f"Sonuç: {sonuc}"
        )

        self.skor_guncelle()
        self.butonsuz_temizle()

        if self.oyun_bitti_mi():
            self.oyun_bitti_ekrani()
            return

        self.devam_btn.setVisible(True)
        self.restart_btn.setVisible(False)

    # -------------------------------------------------
    # SONRAKİ TUR
    # -------------------------------------------------
    def sonraki_tur(self):
        if self.oyun_bitti_mi():
            self.oyun_bitti_ekrani()
            return

        self.oyun.tur += 1
        self.devam_btn.setVisible(False)
        self.kartlari_goster()

    # -------------------------------------------------
    # YENİDEN BAŞLAT
    # -------------------------------------------------
    def yeniden_baslat(self):
        self.oyunu_baslat()

    # -------------------------------------------------
    # ÇIKIŞ
    # -------------------------------------------------
    def cikis(self):
        QApplication.quit()