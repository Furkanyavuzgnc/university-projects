from modeller.sporcu import Sporcu

class Voleybolcu(Sporcu):
    def __init__(self, id, ad, takim, servis, blok, smac, dayaniklilik, enerji, ozel):
        super().__init__(id, ad, takim, enerji, dayaniklilik, ozel)
        self.servis = servis
        self.blok = blok
        self.smac = smac
        self.brans = "voleybol"

    def performans_hesapla(self, ozellik):
        temel = getattr(self, ozellik)

        if self.enerji < 40:
            temel *= 0.8
        elif self.enerji <= 70:
            temel *= 0.9

        return temel + (self.seviye * 5)