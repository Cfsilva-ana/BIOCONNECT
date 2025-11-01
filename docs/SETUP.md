# 🚀 Setup Rápido

## 📦 Instalação
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicação
python app.py

# 3. Acessar
# http://127.0.0.1:8002
```

## 👤 Login de Teste
**Médico:** `medico@teste.com` / `123456`
**Pacientes:** `ESP32_001`, `ESP32_002`, `ESP32_003`

## 🔌 ESP32 Básico
```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";
const char* serverURL = "http://192.168.1.100:8002/api/v1/esp32/data";

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) delay(500);
}

void loop() {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    
    String data = "{\"device_id\":\"ESP32_001\",\"bpm\":72,\"temperature\":36.5}";
    http.POST(data);
    http.end();
    
    delay(30000); // 30 segundos
}
```

## 📁 Estrutura
```
BIOCONNECT/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
├── templates/          # Interface web
├── static/            # CSS/JS
└── docs/              # Documentação
```