import random

class OyunYonetici:

    def __init__(self, kartlar):
        self.kartlar = kartlar
        self.kullanici_kartlar = []
        self.bilgisayar_kartlar = []
        self.tur = 0

        self.skor_kullanici = 0
        self.skor_bilgisayar = 0

        self.moral_kullanici = 50
        self.moral_bilgisayar = 50

        self.tur_sirasi = ["futbol", "basketbol", "voleybol"]

    def kartlari_dagit(self):
        random.shuffle(self.kartlar)
        yarisi = len(self.kartlar) // 2
        self.kullanici_kartlar = self.kartlar[:yarisi]
        self.bilgisayar_kartlar = self.kartlar[yarisi:]

    def moral_bonus(self, moral):
        if moral >= 80:
            return 10
        elif moral >= 50:
            return 5
        else:
            return -5

    def kart_sec_kullanici(self, brans):
        uygun = [k for k in self.kullanici_kartlar if k.brans == brans]

        if not uygun:
            print("Bu branşta kartın yok!")
            return None

        print("\nKartların:")
        for i, k in enumerate(uygun):
            print(f"{i} - {k.ad}")

        secim = int(input("Kart seç: "))
        kart = uygun[secim]

        self.kullanici_kartlar.remove(kart)
        return kart

    def kart_sec_bilgisayar(self, brans, ozellik):
        uygun = [k for k in self.bilgisayar_kartlar if k.brans == brans]

        if not uygun:
            return None

        en_iyi = max(uygun, key=lambda k: k.performans_hesapla(ozellik))
        self.bilgisayar_kartlar.remove(en_iyi)
        return en_iyi

    def ozellik_sec(self, brans):
        if brans == "futbol":
            return random.choice(["penalti", "serbest", "karsi_karsiya"])
        elif brans == "basketbol":
            return random.choice(["ikilik", "ucluk", "serbest"])
        else:
            return random.choice(["servis", "blok", "smac"])

    def tur_oyna(self):
        brans = self.tur_sirasi[self.tur % 3]
        self.tur += 1

        print(f"\n--- TUR {self.tur} ---")
        print(f"Branş: {brans}")

        ozellik = self.ozellik_sec(brans)

        k_kart = self.kart_sec_kullanici(brans)
        b_kart = self.kart_sec_bilgisayar(brans, ozellik)

        if k_kart is None and b_kart is None:
            print("İki oyuncuda da kart yok, tur atlandı")
            return
        elif k_kart is None:
            print("Bilgisayar hükmen kazandı")
            self.skor_bilgisayar += 8
            return
        elif b_kart is None:
            print("Sen hükmen kazandın")
            self.skor_kullanici += 8
            return

        print("Özellik:", ozellik)

        k_puan = (
                k_kart.performans_hesapla(ozellik)
                + self.moral_bonus(self.moral_kullanici)
                + k_kart.ozel_yetenek_bonus(self.tur)
        )

        b_puan = (
                b_kart.performans_hesapla(ozellik)
                + self.moral_bonus(self.moral_bilgisayar)
                + b_kart.ozel_yetenek_bonus(self.tur)
        )
        # defender etkisi
        if k_kart.ozel_yetenek == "Defender":
            b_puan -= 5

        if b_kart.ozel_yetenek == "Defender":
            k_puan -= 5

        print(f"Kullanıcı: {k_kart.ad} ({k_puan})")
        print(f"Bilgisayar: {b_kart.ad} ({b_puan})")

        if k_puan > b_puan:
            print("Kazandın!")
            self.skor_kullanici += 10
            sonuc_k = "kazandi"
            sonuc_b = "kaybetti"
            self.moral_kullanici += 5
            self.moral_bilgisayar -= 5

        elif b_puan > k_puan:
            print("Bilgisayar kazandı!")
            self.skor_bilgisayar += 10
            sonuc_k = "kaybetti"
            sonuc_b = "kazandi"
            self.moral_bilgisayar += 5
            self.moral_kullanici -= 5

        else:
            print("Berabere!")
            sonuc_k = "berabere"
            sonuc_b = "berabere"

        k_kart.enerji_guncelle(sonuc_k)
        b_kart.enerji_guncelle(sonuc_b)

        k_kart.deneyim_kazan(sonuc_k)
        b_kart.deneyim_kazan(sonuc_b)

    def oyunu_baslat(self):
        self.kartlari_dagit()

        while self.kullanici_kartlar or self.bilgisayar_kartlar:
            self.tur_oyna()

        print("\n--- OYUN BİTTİ ---")
        print(f"Kullanıcı: {self.skor_kullanici}")
        print(f"Bilgisayar: {self.skor_bilgisayar}")

