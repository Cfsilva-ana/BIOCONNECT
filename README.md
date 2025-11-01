# 🩺 BioConnect - Plataforma de Monitoramento Biomédico

Sistema completo de monitoramento biomédico em tempo real com ESP32, interface web moderna e dashboard médico profissional.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Uso](#uso)
- [API para ESP32](#api-para-esp32)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dados de Teste](#dados-de-teste)

## 🎯 Visão Geral

O BioConnect é uma plataforma web desenvolvida em FastAPI que permite:
- Monitoramento de pacientes via dispositivos ESP32
- Dashboard médico para acompanhamento de múltiplos pacientes
- Interface moderna e responsiva
- Sistema de alertas críticos com localização
- Perfis detalhados de pacientes

## ✨ Funcionalidades

### 👨‍⚕️ Para Médicos
- **Dashboard Centralizado**: Visão geral de todos os pacientes
- **Lista de Pacientes**: Cards com informações em tempo real
- **Alertas Críticos**: Notificações com localização de emergência
- **Detalhes Completos**: Histórico médico, medicações, contatos
- **Estatísticas**: Resumo geral dos pacientes monitorados

### 👤 Para Pacientes
- **Dashboard Individual**: Monitoramento pessoal
- **Gráficos em Tempo Real**: BPM e temperatura
- **Histórico Pessoal**: Últimas leituras
- **Perfil Completo**: Informações pessoais e dispositivo

### 🔧 Técnicas
- **API REST**: Endpoints para ESP32 e interface web
- **Tempo Real**: Atualização automática de dados
- **Responsivo**: Interface adaptável a todos os dispositivos
- **Seguro**: Validação de dados e autenticação

## 🚀 Instalação

### 1. Pré-requisitos
```bash
Python 3.8+
pip (gerenciador de pacotes Python)
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar Aplicação
```bash
python app.py
```

### 4. Acessar Sistema
- **Interface Web**: http://127.0.0.1:8002
- **API Docs**: http://127.0.0.1:8002/docs

## 📱 Uso

### Login de Teste

**Médico:**
- Email: `medico@teste.com`
- Senha: `123456`

**Pacientes:**
- Device ID: `ESP32_001` (João Silva)
- Device ID: `ESP32_002` (Maria Oliveira)
- Device ID: `ESP32_003` (Carlos Santos)
- Device ID: `ESP32_004` (Ana Costa)
- Device ID: `ESP32_005` (Pedro Lima)

### Navegação
1. **Página Inicial**: Login e registro
2. **Dashboard**: Visão principal (diferente para médicos/pacientes)
3. **Perfil**: Informações pessoais e configurações

## 🔌 API para ESP32

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

### Exemplo ESP32 (Arduino)
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";
const char* serverURL = "http://127.0.0.1:8002/api/v1/esp32/data";
const char* deviceId = "ESP32_001";

void sendData(int bpm, float temperature) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    
    StaticJsonDocument<200> doc;
    doc["device_id"] = deviceId;
    doc["bpm"] = bpm;
    doc["temperature"] = temperature;
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
        Serial.println("Dados enviados com sucesso!");
    }
    
    http.end();
}
```

## 📁 Estrutura do Projeto

```
BIOCONNECT/
├── app.py              # 🚀 Aplicação principal FastAPI
├── requirements.txt    # 📦 Dependências Python
├── templates/          # 🎨 Interface web
│   ├── index.html     # 🏠 Página inicial
│   ├── dashboard.html # 📊 Dashboard
│   └── profile.html   # 👤 Perfil do usuário
├── static/            # 📁 Recursos estáticos
│   ├── css/style.css  # 🎨 Estilos modernos
│   └── js/app.js      # ⚡ JavaScript
├── docs/              # 📚 Documentação
│   ├── API.md         # 📡 API Reference
│   └── SETUP.md       # 🚀 Setup rápido
├── ESP32_SETUP.md     # 🔌 Guia ESP32
├── DEPLOYMENT.md      # 🌐 Deploy produção
└── README.md          # 📖 Documentação principal
```

## 🗂️ Dados de Teste

### Pacientes Cadastrados
| Nome | Device ID | Idade | Condição | Status |
|------|-----------|-------|----------|---------|
| João Silva | ESP32_001 | 45 | Hipertensão | Elevado |
| Maria Oliveira | ESP32_002 | 32 | Diabetes | Normal |
| Carlos Santos | ESP32_003 | 58 | Arritmia | Alto |
| Ana Costa | ESP32_004 | 28 | Saudável | Normal |
| Pedro Lima | ESP32_005 | 67 | Cardiopatia | Crítico |

### Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Página inicial |
| GET | `/dashboard` | Dashboard |
| GET | `/profile` | Perfil do usuário |
| POST | `/api/v1/login` | Autenticação |
| POST | `/api/v1/register` | Registro |
| GET | `/api/v1/patients` | Lista de pacientes |
| POST | `/api/v1/esp32/data` | Receber dados ESP32 |
| GET | `/api/v1/esp32/status/{id}` | Status do dispositivo |

## 🔧 Desenvolvimento

### Adicionar Novo Paciente
```python
users_db["patient_ESP32_XXX"] = {
    "name": "Nome do Paciente",
    "device_id": "ESP32_XXX",
    "type": "patient",
    "age": 30,
    "condition": "Condição Médica",
    # ... outros campos
}
```

### Personalizar Alertas
Edite a função `receive_esp32_data()` em `app.py` para ajustar os limites:
```python
status = "normal" if 60 <= bpm <= 100 and 35.0 <= temperature <= 37.5 else "elevated"
```

## 📚 Documentação Adicional

- **[Setup Rápido](docs/SETUP.md)** - Instalação e configuração básica
- **[API Reference](docs/API.md)** - Documentação completa da API
- **[ESP32 Setup](ESP32_SETUP.md)** - Configuração do hardware
- **[Deploy](DEPLOYMENT.md)** - Guia para produção

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação da API em `/docs`
2. Consulte os logs do servidor
3. Teste os endpoints com dados de exemplo

---

**BioConnect** - Monitoramento Biomédico Inteligente 🩺