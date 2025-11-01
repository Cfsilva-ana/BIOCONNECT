# 📡 API Documentation

Documentação completa da API BioConnect para integração com ESP32.

## 🔗 Base URL
```
http://127.0.0.1:8002/api/v1
```

## 🔌 ESP32 Endpoints

### Enviar Dados
```http
POST /api/v1/esp32/data
Content-Type: application/json

{
    "device_id": "ESP32_001",
    "bpm": 72,
    "temperature": 36.5
}
```

### Verificar Status
```http
GET /api/v1/esp32/status/ESP32_001
```

## 📊 Classificação de Sinais

**BPM:** 60-100 (normal), 101-120 (elevado), >120 (alto)
**Temperatura:** 35.0-37.5°C (normal), >37.5°C (elevado)

## 💻 Exemplo ESP32
```cpp
void sendData(int bpm, float temperature) {
    HTTPClient http;
    http.begin("http://192.168.1.100:8002/api/v1/esp32/data");
    http.addHeader("Content-Type", "application/json");
    
    String payload = "{\"device_id\":\"ESP32_001\",\"bpm\":" + 
                    String(bpm) + ",\"temperature\":" + String(temperature) + "}";
    
    http.POST(payload);
    http.end();
}
```