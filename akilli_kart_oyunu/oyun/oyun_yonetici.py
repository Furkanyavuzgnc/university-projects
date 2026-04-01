import random


class OyunYonetici:
    def __init__(self, kartlar, zorluk="orta"):
        self.kartlar = kartlar
        self.kullanici_kartlar = []
        self.bilgisayar_kartlar = []
        self.tur = 0

        self.skor_kullanici = 0
        self.skor_bilgisayar = 0

        self.moral_kullanici = 50
        self.moral_bilgisayar = 50

        self.tur_sirasi = ["futbol", "basketbol", "voleybol"]
        self.zorluk = zorluk

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

    def kart_sec_bilgisayar(self, brans, ozellik):
        uygun = [k for k in self.bilgisayar_kartlar if k.brans == brans]

        if not uygun:
            return None

        # Zorluk seviyesine göre bilgisayar davranışı
        if self.zorluk == "kolay":
            secilen = random.choice(uygun)

        elif self.zorluk == "orta":
            if random.random() < 0.5:
                secilen = max(uygun, key=lambda k: k.performans_hesapla(ozellik))
            else:
                secilen = random.choice(uygun)

        else:  # zor
            secilen = max(uygun, key=lambda k: k.performans_hesapla(ozellik))

        self.bilgisayar_kartlar.remove(secilen)
        return secilen

    def ozellik_sec(self, brans):
        if brans == "futbol":
            return random.choice(["penalti", "serbest", "karsi_karsiya"])
        elif brans == "basketbol":
            return random.choice(["ikilik", "ucluk", "serbest"])
        else:
            return random.choice(["servis", "blok", "smac"])

    def moral_sinirla(self):
        self.moral_kullanici = max(0, min(100, self.moral_kullanici))
        self.moral_bilgisayar = max(0, min(100, self.moral_bilgisayar))

    def tur_sonucu_hesapla(self, kart):
        brans = self.tur_sirasi[self.tur % 3]
        ozellik = self.ozellik_sec(brans)

        b_kart = self.kart_sec_bilgisayar(brans, ozellik)

        # Bilgisayarın bu branşta kartı yoksa
        if b_kart is None:
            if kart in self.kullanici_kartlar:
                self.kullanici_kartlar.remove(kart)

            self.skor_kullanici += 8

            return {
                "brans": brans,
                "ozellik": ozellik,
                "kullanici_kart": kart,
                "bilgisayar_kart": None,
                "kullanici_puan": 0,
                "bilgisayar_puan": 0,
                "sonuc": "hukmen_kullanici"
            }

        if kart in self.kullanici_kartlar:
            self.kullanici_kartlar.remove(kart)

        k_puan = (
            kart.performans_hesapla(ozellik)
            + self.moral_bonus(self.moral_kullanici)
            + kart.ozel_yetenek_bonus(self.tur + 1)
        )

        b_puan = (
            b_kart.performans_hesapla(ozellik)
            + self.moral_bonus(self.moral_bilgisayar)
            + b_kart.ozel_yetenek_bonus(self.tur + 1)
        )

        if kart.ozel_yetenek == "Defender":
            b_puan -= 5

        if b_kart.ozel_yetenek == "Defender":
            k_puan -= 5

        k_puan = max(0, k_puan)
        b_puan = max(0, b_puan)

        if k_puan > b_puan:
            self.skor_kullanici += 10
            sonuc = "kazandi"
            sonuc_k = "kazandi"
            sonuc_b = "kaybetti"
            self.moral_kullanici += 5
            self.moral_bilgisayar -= 5

        elif b_puan > k_puan:
            self.skor_bilgisayar += 10
            sonuc = "kaybetti"
            sonuc_k = "kaybetti"
            sonuc_b = "kazandi"
            self.moral_bilgisayar += 5
            self.moral_kullanici -= 5

        else:
            sonuc = "berabere"
            sonuc_k = "berabere"
            sonuc_b = "berabere"

        self.moral_sinirla()

        kart.enerji_guncelle(sonuc_k)
        b_kart.enerji_guncelle(sonuc_b)

        kart.deneyim_kazan(sonuc_k)
        b_kart.deneyim_kazan(sonuc_b)

        return {
            "brans": brans,
            "ozellik": ozellik,
            "kullanici_kart": kart,
            "bilgisayar_kart": b_kart,
            "kullanici_puan": k_puan,
            "bilgisayar_puan": b_puan,
            "sonuc": sonuc
        }