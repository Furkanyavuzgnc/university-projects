from modeller.sporcu import Sporcu

class Futbolcu(Sporcu):
    def __init__(self, id, ad, takim, penalti, serbest, karsi_karsiya, dayaniklilik, enerji, ozel):
        super().__init__(id, ad, takim, enerji, dayaniklilik, ozel)
        self.penalti = penalti
        self.serbest = serbest
        self.karsi_karsiya = karsi_karsiya
        self.brans = "futbol"

    def performans_hesapla(self, ozellik):
        temel = getattr(self, ozellik)

        if self.enerji < 40:
            temel *= 0.8
        elif self.enerji <= 70:
            temel *= 0.9

        return temel + (self.seviye * 5)