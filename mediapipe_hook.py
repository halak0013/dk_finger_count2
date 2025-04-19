
import os
import sys
import tempfile
import shutil

# MediaPipe için gerekli olan modül ve dosyaları _MEIPASS'den kopyala
def setup_mediapipe():
    # _MEIPASS varsa, PyInstaller tarafından oluşturulan geçici dizindir
    if hasattr(sys, '_MEIPASS'):
        src_dir = os.path.join(sys._MEIPASS, 'mediapipe')
        if os.path.exists(src_dir):
            # Geçici bir klasör oluştur
            mediapipe_temp = os.path.join(tempfile.gettempdir(), 'mediapipe_temp')
            
            # Önceki klasör varsa temizle
            if os.path.exists(mediapipe_temp):
                try:
                    shutil.rmtree(mediapipe_temp)
                except:
                    pass
            
            # MediaPipe dosyalarını geçici dizine kopyala
            try:
                shutil.copytree(src_dir, mediapipe_temp)
                # Bu geçici dizini modül arama yoluna ekle
                if mediapipe_temp not in sys.path:
                    sys.path.insert(0, os.path.dirname(mediapipe_temp))
                    
                print(f"MediaPipe kaynakları başarıyla çıkarıldı: {mediapipe_temp}")
            except Exception as e:
                print(f"MediaPipe dosyalarını çıkarırken hata: {e}")

setup_mediapipe()
