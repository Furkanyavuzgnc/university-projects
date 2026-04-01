from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QApplication,
    QMessageBox, QHBoxLayout
)
from veri.veri_okuyucu import VeriOkuyucu
from oyun.oyun_yonetici import OyunYonetici


class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Akıllı Kart Oyunu")
        self.setGeometry(200, 200, 600, 700)

        self.layout = QVBoxLayout()

        self.skor_label = QLabel()
        self.skor_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 8px;")
        self.layout.addWidget(self.skor_label)

        self.label = QLabel("Zorluk seçerek oyuna başla.")
        self.label.setStyleSheet("font-size: 15px; padding: 10px;")
        self.layout.addWidget(self.label)

        # Zorluk seçim alanı
        self.zorluk_layout = QHBoxLayout()

        self.kolay_btn = QPushButton("Kolay")
        self.kolay_btn.clicked.connect(lambda: self.oyunu_baslat("kolay"))

        self.orta_btn = QPushButton("Orta")
        self.orta_btn.clicked.connect(lambda: self.oyunu_baslat("orta"))

        self.zor_btn = QPushButton("Zor")
        self.zor_btn.clicked.connect(lambda: self.oyunu_baslat("zor"))

        for btn in [self.kolay_btn, self.orta_btn, self.zor_btn]:
            btn.setStyleSheet("padding: 10px; font-weight: bold;")
            self.zorluk_layout.addWidget(btn)

        self.layout.addLayout(self.zorluk_layout)

        self.kart_layout = QVBoxLayout()
        self.layout.addLayout(self.kart_layout)

        self.bilgisayar_kartlari_btn = QPushButton("🖥 Bilgisayarın Kartlarını Göster")
        self.bilgisayar_kartlari_btn.clicked.connect(self.bilgisayar_kartlarini_goster)
        self.bilgisayar_kartlari_btn.setVisible(False)
        self.bilgisayar_kartlari_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        self.layout.addWidget(self.bilgisayar_kartlari_btn)

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
        self.oyun = None
        self.secilen_zorluk = None

    # -------------------------------------------------
    # OYUN BAŞLAT
    # -------------------------------------------------
    def oyunu_baslat(self, zorluk):
        self.secilen_zorluk = zorluk

        kartlar = VeriOkuyucu.oku("veri/sporcular.txt")
        self.oyun = OyunYonetici(kartlar, zorluk=zorluk)
        self.oyun.kartlari_dagit()
        self.oyun.tur = 0

        self.butonsuz_temizle()

        self.devam_btn.setVisible(False)
        self.restart_btn.setVisible(False)
        self.bilgisayar_kartlari_btn.setVisible(True)

        # oyun başladıktan sonra zorluk butonları gizlensin
        self.kolay_btn.setVisible(False)
        self.orta_btn.setVisible(False)
        self.zor_btn.setVisible(False)

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
        if self.oyun:
            self.skor_label.setText(
                f"Skor: Kullanıcı {self.oyun.skor_kullanici} - {self.oyun.skor_bilgisayar} Bilgisayar"
            )
        else:
            self.skor_label.setText("Skor: Kullanıcı 0 - 0 Bilgisayar")

    def bilgisayar_kartlarini_goster(self):
        if not self.oyun:
            return

        if not self.oyun.bilgisayar_kartlar:
            QMessageBox.information(self, "Bilgisayar Kartları", "Bilgisayarın elinde kart kalmadı.")
            return

        metin = ""
        for kart in self.oyun.bilgisayar_kartlar:
            metin += (
                f"Ad: {kart.ad}\n"
                f"Branş: {kart.brans}\n"
                f"Enerji: {kart.enerji}\n"
                f"Seviye: {kart.seviye}\n"
                f"----------------------\n"
            )

        QMessageBox.information(self, "Bilgisayarın Elindeki Kartlar", metin)

    # -------------------------------------------------
    # OYUN BİTİŞ
    # -------------------------------------------------
    def oyun_bitti_mi(self):
        return self.oyun and (not self.oyun.kullanici_kartlar) and (not self.oyun.bilgisayar_kartlar)

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
            f"Zorluk: {self.secilen_zorluk.upper()}\n\n"
            f"{sonuc}\n\n"
            f"Final Skoru:\n"
            f"Kullanıcı: {self.oyun.skor_kullanici}\n"
            f"Bilgisayar: {self.oyun.skor_bilgisayar}"
        )

        self.devam_btn.setVisible(False)
        self.restart_btn.setVisible(True)
        self.bilgisayar_kartlari_btn.setVisible(False)

    # -------------------------------------------------
    # KARTLARI GÖSTER
    # -------------------------------------------------
    def kartlari_goster(self):
        if self.oyun_bitti_mi():
            self.oyun_bitti_ekrani()
            return

        self.butonsuz_temizle()

        brans = self.oyun.tur_sirasi[self.oyun.tur % 3]
        self.label.setText(
            f"Zorluk: {self.secilen_zorluk.upper()}\n"
            f"Sıradaki Branş: {brans.upper()}\n"
            f"Lütfen bir kart seç."
        )

        uygun_kartlar = [k for k in self.oyun.kullanici_kartlar if k.brans == brans]
        uygun_bilgisayar = [k for k in self.oyun.bilgisayar_kartlar if k.brans == brans]

        if not uygun_kartlar:
            if not uygun_bilgisayar:
                self.label.setText(
                    f"Zorluk: {self.secilen_zorluk.upper()}\n"
                    f"Sıradaki Branş: {brans.upper()}\n"
                    "Bu branşta iki tarafta da kart yok. Tur otomatik atlandı."
                )
            else:
                self.label.setText(
                    f"Zorluk: {self.secilen_zorluk.upper()}\n"
                    f"Sıradaki Branş: {brans.upper()}\n"
                    "Bu branşta kartın yok. Bilgisayar hükmen kazandı."
                )
                self.oyun.skor_bilgisayar += 8

                bilgisayar_karti = uygun_bilgisayar[0]
                if bilgisayar_karti in self.oyun.bilgisayar_kartlar:
                    self.oyun.bilgisayar_kartlar.remove(bilgisayar_karti)

                self.skor_guncelle()

            self.devam_btn.setVisible(True)
            self.restart_btn.setVisible(False)
            return

        for kart in uygun_kartlar:
            btn = QPushButton(
                f"{kart.ad} | Enerji: {kart.enerji} | Seviye: {kart.seviye}"
            )
            btn.setStyleSheet(self.renk_getir(kart.brans))
            btn.clicked.connect(lambda checked, k=kart: self.kart_sec(k))
            self.kart_layout.addWidget(btn)
            self.butonlar.append(btn)

    # -------------------------------------------------
    # KART SEÇ
    # -------------------------------------------------
    def kart_sec(self, kart):
        sonuc = self.oyun.tur_sonucu_hesapla(kart)

        if sonuc["sonuc"] == "hukmen_kullanici":
            self.label.setText(
                f"Branş: {sonuc['brans'].upper()}\n"
                f"Seçtiğin Kart: {sonuc['kullanici_kart'].ad}\n\n"
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

        sonuc_yazi = {
            "kazandi": "🎉 Kazandın!",
            "kaybetti": "❌ Kaybettin!",
            "berabere": "🤝 Berabere!"
        }

        self.label.setText(
            f"Branş: {sonuc['brans'].upper()}\n"
            f"Özellik: {sonuc['ozellik']}\n\n"
            f"Senin Kartın: {sonuc['kullanici_kart'].ad} | Puan: {sonuc['kullanici_puan']}\n"
            f"Bilgisayar Kartı: {sonuc['bilgisayar_kart'].ad} | Puan: {sonuc['bilgisayar_puan']}\n\n"
            f"Sonuç: {sonuc_yazi[sonuc['sonuc']]}"
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
        self.oyun = None
        self.secilen_zorluk = None

        self.butonsuz_temizle()
        self.label.setText("Zorluk seçerek oyuna başla.")
        self.skor_guncelle()

        self.devam_btn.setVisible(False)
        self.restart_btn.setVisible(False)
        self.bilgisayar_kartlari_btn.setVisible(False)

        self.kolay_btn.setVisible(True)
        self.orta_btn.setVisible(True)
        self.zor_btn.setVisible(True)

    # -------------------------------------------------
    # ÇIKIŞ
    # -------------------------------------------------
    def cikis(self):
        QApplication.quit()