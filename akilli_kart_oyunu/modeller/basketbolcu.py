from modeller.sporcu import Sporcu

class Basketbolcu(Sporcu):
    def __init__(self, id, ad, takim, ikilik, ucluk, serbest, dayaniklilik, enerji, ozel):
        super().__init__(id, ad, takim, enerji, dayaniklilik, ozel)
        self.ikilik = ikilik
        self.ucluk = ucluk
        self.serbest = serbest
        self.brans = "basketbol"

    def performans_hesapla(self, ozellik):
        temel = getattr(self, ozellik)

        if self.enerji < 40:
            temel *= 0.8
        elif self.enerji <= 70:
            temel *= 0.9

        return temel + (self.seviye * 5)