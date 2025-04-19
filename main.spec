# -*- mode: python ; coding: utf-8 -*-
import os
import mediapipe as mp
import tempfile

block_cipher = None

# MediaPipe modül dizinini bul
mediapipe_path = os.path.dirname(mp.__file__)

# MediaPipe dosyalarını işlemek için özel runtime hook oluştur
with open('mediapipe_hook.py', 'w') as f:
    f.write('''
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
''')

# Dışa aktarılacak tüm veri dosyalarını tanımlama
added_files = [
    ('app_data', 'app_data'),  # Tüm klasörü kopyala
    ('LICENSE', '.'),
    ('readme.md', '.'),
    # MediaPipe içeriğini ekle
    (mediapipe_path, 'mediapipe')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'PyQt6', 
        'PyQt6.QtWidgets', 
        'PyQt6.QtCore', 
        'PyQt6.QtGui',
        'opencv-python',
        'mediapipe',
        'numpy',
        'cvzone',
        'cvzone.HandTrackingModule',
        'pyyaml',
        'yaml'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['mediapipe_hook.py'],  # Özel hook'u ekle
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DK',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Hata ayıklama için konsolu açık bırak, çalıştığında False yapabilirsiniz
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_data/icon.png',
    onefile=True
)