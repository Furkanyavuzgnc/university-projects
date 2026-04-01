from modeller.futbolcu import Futbolcu
from modeller.basketbolcu import Basketbolcu
from modeller.voleybolcu import Voleybolcu

class VeriOkuyucu:

    @staticmethod
    def oku(dosya):
        kartlar = []

        with open(dosya, "r", encoding="utf-8") as f:
            for i, satir in enumerate(f):
                veri = satir.strip().split(",")

                if veri[0] == "futbol":
                    kart = Futbolcu(
                        i, veri[1], veri[2],
                        int(veri[3]), int(veri[4]), int(veri[5]),
                        int(veri[6]), int(veri[7]), veri[8]
                    )

                elif veri[0] == "basketbol":
                    kart = Basketbolcu(
                        i, veri[1], veri[2],
                        int(veri[3]), int(veri[4]), int(veri[5]),
                        int(veri[6]), int(veri[7]), veri[8]
                    )

                elif veri[0] == "voleybol":
                    kart = Voleybolcu(
                        i, veri[1], veri[2],
                        int(veri[3]), int(veri[4]), int(veri[5]),
                        int(veri[6]), int(veri[7]), veri[8]
                    )

                else:
                    continue

                kartlar.append(kart)

        return kartlar