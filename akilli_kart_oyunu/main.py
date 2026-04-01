import sys
from PyQt5.QtWidgets import QApplication
from arayuz.main_window import AnaPencere


def main():
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()