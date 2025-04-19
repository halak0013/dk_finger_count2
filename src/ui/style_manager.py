import os
import sys

def resource_path(relative_path):
    """PyInstaller ile paketlenmiş uygulamada doğru dosya yolunu bulur"""
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class StyleManager:
    def __init__(self):
        # Varsayılan yeşil tema renkleri
        self.colors = {
            "MAIN_BG": "#08110b",
            "SECONDARY_BG": "#162117",
            "ACCENT": "#2e7d32",
            "ACCENT_HOVER": "#388e3c",
            "ACCENT_PRESSED": "#1b5e20",
            "TEXT": "#e8f5e9",
            "BORDER": "#4c8c4a",
            "DISABLED_BG": "#2e3b31",
            "DISABLED_TEXT": "#8aa28b",
            "START_BUTTON": "#1b813e",
            "START_BUTTON_HOVER": "#259d4a",
            "STOP_BUTTON": "#c62828",
            "STOP_BUTTON_HOVER": "#e53935",
            "SAVE_BUTTON": "#00695c",
            "EXIT_BUTTON": "#37474f",
        }

    def load_qss(self, file_path="app_data/style.qss"):
        """QSS dosyasını yükler ve içindeki değişkenleri mevcut tema renklerine göre değiştirir"""
        try:
            # resource_path fonksiyonu ile gerçek dosya yolunu al
            actual_path = resource_path(file_path)
            with open(actual_path, "r", encoding="utf-8") as file:
                qss_content = file.read()

            # ${VARIABLE} formatındaki değişkenleri değiştir
            for color_name, color_value in self.colors.items():
                placeholder = "${" + color_name + "}"
                qss_content = qss_content.replace(placeholder, color_value)

            return qss_content

        except Exception as e:
            print(f"QSS dosyası yüklenirken hata: {e}")
            return ""

    def get_styled_qss(self):
        """Mevcut tema renklerine göre biçimlendirilmiş QSS stringini döndürür"""
        return self.load_qss()

    def update_color(self, color_name, color_value):
        """Belirli bir rengi günceller"""
        if color_name in self.colors:
            self.colors[color_name] = color_value

    def set_green_theme(self):
        """Green theme colors"""
        self.colors.update(
            {
                "MAIN_BG": "#00140b",  # Rich Black
                "SECONDARY_BG": "#03221A",  # Dark Green
                "ACCENT": "#2CC295",  # Mountain Meadow
                "ACCENT_HOVER": "#00FFB3",  # Caribbean Green
                "ACCENT_PRESSED": "#00A37A",  # Darker Caribbean Green
                "TEXT": "#F1FFF6",  # Anti-Flash White
                "BORDER": "#2CC295",  # Mountain Meadow
                "DISABLED_BG": "#063820",  # Pine
                "DISABLED_TEXT": "#8AA28B",  # Muted Green
                "START_BUTTON": "#2CC295",  # Mountain Meadow
                "START_BUTTON_HOVER": "#00FFB3",  # Caribbean Green
                "STOP_BUTTON": "#C62828",  # Red for Stop
                "STOP_BUTTON_HOVER": "#E53935",  # Lighter Red
                "SAVE_BUTTON": "#00695C",  # Teal
                "EXIT_BUTTON": "#37474F",  # Grayish Blue
            }
        )

    def set_blue_theme(self):
        """Mavi tema renklerini ayarlar"""
        self.colors.update(
            {
                "MAIN_BG": "#2d2d30",
                "SECONDARY_BG": "#252526",
                "ACCENT": "#007acc",
                "ACCENT_HOVER": "#0085e5",
                "ACCENT_PRESSED": "#005fa3",
                "TEXT": "#e0e0e0",
                "BORDER": "#007acc",
                "DISABLED_BG": "#3d3d3d",
                "DISABLED_TEXT": "#858585",
                "START_BUTTON": "#28a745",
                "START_BUTTON_HOVER": "#2fc751",
                "STOP_BUTTON": "#dc3545",
                "STOP_BUTTON_HOVER": "#e84c5a",
                "SAVE_BUTTON": "#17a2b8",
                "EXIT_BUTTON": "#6c757d",
            }
        )