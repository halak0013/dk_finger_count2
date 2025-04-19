from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QComboBox,
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap

from src.processor.main_processor import ProcessorThread
from src.utils.config_helper import Config
from src.ui.custom_widgets import CustomSlider, CustomSpiner
from src.ui.style_manager import StyleManager


class MainWindow(QMainWindow):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.parameters()

        self.setWindowTitle("Dk")
        self.setGeometry(100, 100, 800, 500)

        # Ana widget oluşturma
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Ana düzen
        self.main_layout = QHBoxLayout(self.central_widget)

        # Kamera görüntüsü için label (sol taraf)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet("border: 1px solid black;")

        # Butonlar için düzen (sağ taraf)
        self.controls_layout = QVBoxLayout()

        self.camera_ui_cofigurations()
        self.setup_theme_section()

        # Düzen boşluğu ekleyerek butonları üstte topla
        self.controls_layout.addStretch()

        # Ana düzene bileşenleri ekle
        self.main_layout.addWidget(self.image_label, 4)  # 4/5 oranında sol taraf
        self.main_layout.addLayout(self.controls_layout, 1)  # 1/5 oranında sağ taraf

        # Kamera thread'ini oluştur
        self.kamera_thread = ProcessorThread(self.config)
        self.kamera_thread.frame_updated.connect(self.update_frame)

    def parameters(self):
        self.set_val = lambda value, variable: setattr(self.config, variable, value)
        self.style_manager = StyleManager()
        self.style_manager.set_green_theme()
        self.apply_theme()

    def apply_theme(self):
        """Mevcut temayı uygula"""
        qss_string = self.style_manager.get_styled_qss()
        self.setStyleSheet(qss_string)

    def handle_theme_change(self, theme_text):
        """Tema değiştiğinde çağrılır"""
        if theme_text == "Yeşil Tema":
            self.style_manager.set_green_theme()
        else:
            self.style_manager.set_blue_theme()

        # Temayı değiştirdikten sonra yeniden uygula
        self.apply_theme()

    def setup_theme_section(self):

        self.cmb_theme = QComboBox()
        self.cmb_theme.addItems(["Yeşil Tema", "Mavi Tema"])
        self.cmb_theme.currentTextChanged.connect(self.handle_theme_change)

        self.controls_layout.addWidget(self.cmb_theme)

    def camera_ui_cofigurations(self):
        self.btn_start_camera = QPushButton("Kamerayı Aç")
        self.btn_start_camera.clicked.connect(self.start_camera)
        self.controls_layout.addWidget(self.btn_start_camera)

        self.btn_stop_camera = QPushButton("Kamerayı Kapat")
        self.btn_stop_camera.clicked.connect(self.stop_camera)
        self.btn_stop_camera.setEnabled(False)
        self.controls_layout.addWidget(self.btn_stop_camera)

        self.btn_exit = QPushButton("Çıkış")
        self.btn_exit.clicked.connect(self.close)
        self.controls_layout.addWidget(self.btn_exit)

        self.btn_save = QPushButton("Ayarları Kaydet")
        self.btn_save.clicked.connect(self.config.to_yaml)
        self.controls_layout.addWidget(self.btn_save)

        self.spn_camera_index = CustomSpiner(
            "Kamera İndeks", 0, 4, self.config.camera_index, 1, self.change_camera_index
        )
        self.controls_layout.addWidget(self.spn_camera_index)

        self.sld_camera_width = CustomSlider(
            "Kamera Genişliği", 320, 1920, 640, 100, self.change_camera_width
        )
        self.controls_layout.addWidget(self.sld_camera_width)

        self.sld_camera_height = CustomSlider(
            "Kamera Yüksekliği", 320, 1920, 640, 100, self.change_camera_height
        )
        self.controls_layout.addWidget(self.sld_camera_height)
        self.controls_layout.addWidget(QWidget())


    def change_camera_width(self, value):
        self.config.camera_width = value
        self.kamera_thread.stop_camera()

    def change_camera_height(self, value):
        self.config.camera_height = value
        self.kamera_thread.stop_camera()

    def change_camera_index(self, value):
        self.config.camera_index = value
        self.kamera_thread.stop_camera()

    @pyqtSlot(QImage)
    def update_frame(self, qt_image):
        # Görüntüyü etiket boyutuna ölçeklendir
        scaled_image = qt_image.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        # Görüntüyü etikette göster
        self.image_label.setPixmap(QPixmap.fromImage(scaled_image))

    def start_camera(self):
        self.kamera_thread.start_camera()
        self.btn_start_camera.setEnabled(False)
        self.btn_stop_camera.setEnabled(True)

    def stop_camera(self):
        self.kamera_thread.stop_camera()
        self.btn_start_camera.setEnabled(True)
        self.btn_stop_camera.setEnabled(False)
        self.image_label.clear()

    def closeEvent(self, event):
        # Uygulama kapatılırken kamera thread'ini durdur
        self.kamera_thread.stop_camera()
        event.accept()
