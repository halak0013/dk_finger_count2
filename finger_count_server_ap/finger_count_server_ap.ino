#include <WiFi.h>
#include <WiFiUdp.h>
#include <esp_wifi.h>

const char* ssid = "DeneyapKartAP";
const char* password = "12345678.";

const char* udpAddress = "0.0.0.0";  // UDP istemcisinin IP adresi
const int udpPort = 14537;

int fingers[5] = { 0, 0, 0, 0, 0 };
int lights[5] = { D9, D12, D13, D14, D15 };  // Deneyap Kart
// int lights[] = {D13, D14, D12, D10, A7 };  // Deneyap Kart 1A v2
// int lights[] = {D2, D3, D4, D5, D6 };  // Deneyap Mini v2

WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  Serial.println("Başladı");

  Serial.begin(115200);
  delay(2000);
  // ESP32'yi Access Point olarak başlat
  WiFi.softAP(ssid, password);
  Serial.println("Access Point olusturuldu.");
  Serial.print("IP Adresi: ");
  Serial.println(WiFi.softAPIP());

  Serial.println("WiFi'ye bağlanıldı");
  Serial.println(WiFi.localIP());

  // Pin çıkışları ayarlanıyor
  for (int i = 0; i < 5; i++) {
    pinMode(lights[i], OUTPUT);
    digitalWrite(lights[i], LOW);
  }

  // UDP'yi başlat
  udp.begin(udpPort);

  xTaskCreate(receiveDataTask, "ReceiveUdpData", 8096, NULL, 1, NULL);
}

void loop() {
  delay(1000);
}

void receiveDataTask(void* parameter) {
  char incomingPacket[255];  // Gelen veriyi saklamak için buffer
  while (true) {
    // Gelen UDP paketlerinin olup olmadığını kontrol et
    int packetSize = udp.parsePacket();
    if (packetSize) {
      // Paket boyutunu ve gönderici bilgilerini al
      Serial.printf("Paket boyutu: %d\n", packetSize);
      int len = udp.read(incomingPacket, 255);  // Gelen veriyi buffer'a oku
      if (len > 0) {
        incomingPacket[len] = 0;  // String sonu null karakteri ekle
      }

      Serial.printf("Gelen UDP verisi: %s\n", incomingPacket);  // Veriyi ekrana yazdır
      parseUDPData(incomingPacket, fingers);
      for (int i = 0; i < 5; i++) {
        Serial.print("Parmak ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(fingers[i]);
      }
      finger_to_light();

      vTaskDelay(10 / portTICK_PERIOD_MS);  // 30 fps için 33ms bekle
    }
  }
}


void parseUDPData(const char* udpData, int fingers[5]) {
  // Köşeli parantezleri ve boşlukları temizle
  char dataCopy[50];                                 
  strncpy(dataCopy, udpData, sizeof(dataCopy) - 1);  
  dataCopy[sizeof(dataCopy) - 1] = '\0';             

  // Köşeli parantezleri kaldır
  char* cleanData = dataCopy;
  if (cleanData[0] == '[') {
    cleanData++; // İlk karakteri atla
  }
  
  // Son parantezi kaldır
  int len = strlen(cleanData);
  if (len > 0 && cleanData[len-1] == ']') {
    cleanData[len-1] = '\0';
  }

  // Veriyi virgüllerle ayır
  char* token = strtok(cleanData, ",");
  int index = 0;

  // Veriyi int'e çevirip fingers dizisine at
  while (token != nullptr && index < 5) {
    // Boşlukları atla
    while (*token == ' ') {
      token++;
    }
    fingers[index] = atoi(token);  // String'i int'e dönüştür
    token = strtok(nullptr, ",");  // Bir sonraki kısmı al
    index++;
  }
}

void finger_to_light() {
  for (int i = 0; i < 5; i++) {
    if (fingers[i] == 1) {
      digitalWrite(lights[i], HIGH);
    } else {
      digitalWrite(lights[i], LOW);
    }
  }
}
