# sys modülü: uygulamanın sistemle etkileşimini sağlar (örneğin programdan çıkış)
import sys

# PyQt5'ten QApplication sınıfını alıyoruz
# QApplication: GUI uygulamasının ana kontrol sınıfıdır
from PyQt5.QtWidgets import QApplication

# Kendi oluşturduğumuz ana pencere sınıfını import ediyoruz
from arayuz.main_window import AnaPencere


# QApplication nesnesi oluşturulur
# sys.argv: komut satırı argümanlarını alır (genelde boş ama gerekli)
app = QApplication(sys.argv)


# Ana pencere (oyun ekranı) oluşturulur
pencere = AnaPencere()


# Pencereyi ekranda gösterir
pencere.show()


# Uygulamanın çalışmasını başlatır
# exec_(): event loop başlatır (buton tıklamaları vs burada çalışır)
# sys.exit(): program düzgün şekilde kapanır
sys.exit(app.exec_())