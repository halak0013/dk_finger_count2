import yaml
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

class YamlSerializable:
    """YAML serileştirme özellikleri sunan mixin sınıf"""
    yaml_path = "app_data/config.yaml"
    
    @classmethod
    def from_yaml(cls):
        """YAML dosyasından nesne oluşturur"""
        # Resource path kullanarak dosya yolunu düzelt
        file_path = resource_path(cls.yaml_path)
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            # Sınıf bilgisini kaldırıp, geri kalan değerleri kullanarak nesne oluştur
            class_name = data.pop("__class__", None)
            obj = cls()
            for key, value in data.items():
                setattr(obj, key, value)
            return obj
    
    def to_yaml(self):
        """Nesneyi YAML dosyasına kaydeder"""
        # __dict__ kullanarak tüm instance değişkenlerini al ve sınıf adını ekle
        data = self.__dict__.copy()
        data["__class__"] = self.__class__.__name__
        
        # Resource path kullanmıyoruz çünkü yazma genellikle gerçek dosya sistemine yapılır
        # Ancak paketlenmiş uygulamada yazma işlemi için farklı bir strateji gerekebilir
        # Bu durumda kullanıcının yazma iznine sahip olduğu bir klasör seçilmelidir
        # Örneğin: AppData, kullanıcı belgeleri vb.
        try:
            with open(self.yaml_path, "w", encoding="utf-8") as file:
                yaml.dump(data, file, default_flow_style=False)
        except PermissionError:
            # Paketlenmiş uygulamada yazma izni yoksa alternatif bir konum kullanın
            user_data_dir = os.path.join(os.path.expanduser("~"), "DK_App_Data")
            os.makedirs(user_data_dir, exist_ok=True)
            alternative_path = os.path.join(user_data_dir, os.path.basename(self.yaml_path))
            
            with open(alternative_path, "w", encoding="utf-8") as file:
                yaml.dump(data, file, default_flow_style=False)