import yaml


class YamlSerializable:
    """YAML serileştirme özellikleri sunan mixin sınıf"""

    yaml_path = "app_data/config.yaml"

    @classmethod
    def from_yaml(cls):
        """YAML dosyasından nesne oluşturur"""

        with open(cls.yaml_path, "r", encoding="utf-8") as file:
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

        with open(self.yaml_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False)
