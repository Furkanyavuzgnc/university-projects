from abc import ABC, abstractmethod

class Sporcu(ABC):
    def __init__(self, id, ad, takim, enerji, dayaniklilik, ozel_yetenek):
        self.id = id
        self.ad = ad
        self.takim = takim
        self.enerji = enerji
        self.max_enerji = enerji
        self.dayaniklilik = dayaniklilik
        self.seviye = 1
        self.deneyim = 0
        self.ozel_yetenek = ozel_yetenek
        self.brans = None

        self.ozel_kullanildi = False  # tek kullanımlık yetenekler için

    @abstractmethod
    def performans_hesapla(self, ozellik):
        pass

    def enerji_guncelle(self, sonuc):
        if sonuc == "kazandi":
            self.enerji -= 5
        elif sonuc == "kaybetti":
            self.enerji -= 10
        else:
            self.enerji -= 3

        if self.enerji < 0:
            self.enerji = 0

    def deneyim_kazan(self, sonuc):
        if sonuc == "kazandi":
            self.deneyim += 2
        elif sonuc == "berabere":
            self.deneyim += 1

        self.seviye_kontrol()

    def seviye_kontrol(self):
        if self.deneyim >= 8:
            self.seviye = 3
        elif self.deneyim >= 4:
            self.seviye = 2

    # 🔥 ÖZEL YETENEK
    def ozel_yetenek_bonus(self, tur):
        if self.ozel_yetenek == "Clutch":
            if tur >= 5:
                return 10

        elif self.ozel_yetenek == "Finisher":
            if self.enerji < 40:
                return 8

        elif self.ozel_yetenek == "Legend":
            if not self.ozel_kullanildi:
                self.ozel_kullanildi = True
                return 20

        return 0