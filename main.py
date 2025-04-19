#Bismillahirrahmanirrahim
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.ui.main_window import MainWindow
from src.utils.config_helper import Config


if __name__ == "__main__":
    config = Config.from_yaml()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("app_data/icon.png"))
    window = MainWindow(config=config)
    window.show()
    sys.exit(app.exec())
