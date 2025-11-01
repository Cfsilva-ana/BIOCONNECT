# 🩺 BioConnect - Sistema de Monitoramento Biomédico em Tempo Real

![BioConnect](https://img.shields.io/badge/BioConnect-v2.0-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red) ![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen) ![ESP32](https://img.shields.io/badge/ESP32-IoT-orange)

Sistema completo de monitoramento biomédico que integra dispositivos ESP32 com sensores ECG para monitoramento cardíaco em tempo real, dashboard médico profissional e sistema de alertas críticos com localização de emergência.

## 🎯 Visão Geral

O BioConnect é uma plataforma IoT médica que permite:
- **Monitoramento cardíaco em tempo real** via ESP32 + sensor ECG (AD620)
- **Dashboard médico profissional** para acompanhamento de múltiplos pacientes
- **Sistema de alertas críticos** com localização GPS para emergências
- **Histórico completo** de sinais vitais e estatísticas médicas
- **Interface web moderna** e responsiva para médicos e pacientes

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐    MongoDB    ┌─────────────────┐
│   ESP32 + ECG   │ ──────────────► │   FastAPI API    │ ────────────► │  MongoDB Atlas  │
│   (Hardware)    │                 │   (Backend)      │               │   (Database)    │
└─────────────────┘                 └──────────────────┘               └─────────────────┘
                                             │
                                             │ HTTP/WebSocket
                                             ▼
                                    ┌──────────────────┐
                                    │   Web Dashboard  │
                                    │   (Frontend)     │
                                    └──────────────────┘
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **Python 3.8+** - Linguagem principal
- **Motor** - Driver assíncrono para MongoDB
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

### Frontend
- **HTML5/CSS3** - Interface moderna
- **JavaScript ES6+** - Funcionalidades dinâmicas
- **Chart.js** - Gráficos em tempo real
- **Font Awesome** - Ícones profissionais
- **CSS Grid/Flexbox** - Layout responsivo

### Database
- **MongoDB Atlas** - Banco de dados NoSQL na nuvem
- **Coleções**: `users`, `readings`
- **Índices otimizados** para consultas rápidas

### Hardware/IoT
- **ESP32** - Microcontrolador WiFi
- **AD620** - Amplificador de instrumentação para ECG
- **Sensores** - Temperatura e frequência cardíaca
- **WiFi** - Comunicação sem fio

## 📁 Estrutura do Projeto

```
BIOCONNECT/
├── 📄 app.py                    # Aplicação FastAPI principal
├── 📄 requirements.txt          # Dependências Python
├── 📄 create_patients.py        # Script para popular MongoDB
├── 📄 README.md                 # Documentação principal
├── 📁 templates/
│   ├── 📄 dashboard.html        # Dashboard médico/paciente
│   └── 📄 index.html           # Página inicial
├── 📁 static/
│   ├── 📁 css/
│   │   └── 📄 style.css        # Estilos modernos
│   └── 📁 js/
│       └── 📄 app.js           # JavaScript do dashboard
└── 📁 hardware/
    └── 📄 esp32_ecg.ino        # Código Arduino para ESP32
```

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
```bash
Python 3.8+
MongoDB Atlas (conta gratuita)
Arduino IDE (para ESP32)
ESP32 DevKit
Sensor AD620 + componentes ECG
```

### 2. Configuração do Backend
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/bioconnect.git
cd bioconnect

# Instale as dependências
pip install -r requirements.txt

# Configure a string de conexão MongoDB no app.py
MONGO_URL = "sua_string_de_conexao_mongodb_atlas"

# Execute a aplicação
python app.py
```

### 3. Configuração do Hardware
```cpp
// Configure no esp32_ecg.ino
const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";
const char* serverURL = "http://SEU_IP:8002/api/v1/esp32/data";
const char* deviceId = "ESP32_001"; // ID único do dispositivo
```

### 4. Inicialização do Banco de Dados
```bash
# Popule o MongoDB com dados de teste
python create_patients.py
```

## 🔌 API Endpoints

### Autenticação
- `POST /api/v1/login` - Login médico/paciente
- `POST /api/v1/register` - Registro de usuários

### Pacientes
- `GET /api/v1/patients` - Lista todos os pacientes
- `GET /api/v1/patients/{id}/details` - Detalhes completos do paciente
- `GET /api/v1/patients/{id}/history` - Histórico de leituras

### ESP32/IoT
- `POST /api/v1/esp32/data` - Recebe dados dos sensores
- `GET /api/v1/esp32/status/{device_id}` - Status do dispositivo

### Leituras
- `GET /api/v1/readings` - Últimas leituras gerais
- `GET /api/v1/readings/{device_id}` - Leituras de um dispositivo

## 👥 Usuários de Teste

### Médico
- **Email**: `medico@teste.com`
- **Senha**: `123456`

### Pacientes (Device IDs)
| Nome | Device ID | Idade | Condição | Status |
|------|-----------|-------|----------|---------|
| Roberto Mendes | ESP32_006 | 72 | Infarto Agudo | 🔴 Crítico |
| João Silva | ESP32_001 | 45 | Hipertensão | 🟡 Elevado |
| Maria Oliveira | ESP32_002 | 32 | Diabetes Tipo 2 | 🟢 Normal |
| Carlos Santos | ESP32_003 | 58 | Arritmia | 🟡 Elevado |
| Ana Costa | ESP32_004 | 28 | Saudável | 🟢 Normal |
| Pedro Lima | ESP32_005 | 67 | Cardiopatia | 🟢 Normal |

## 🎛️ Funcionalidades Principais

### 👨‍⚕️ Dashboard Médico
- **Lista de Pacientes**: Cards com sinais vitais em tempo real
- **Alertas Críticos**: Notificações com localização GPS
- **Histórico Detalhado**: Timeline de leituras com status
- **Perfis Completos**: Informações médicas, medicações, contatos
- **Estatísticas**: Resumo geral dos pacientes monitorados
- **Botão Emergência**: Acesso rápido à localização de pacientes críticos

### 👤 Dashboard Paciente
- **Monitoramento Pessoal**: BPM e temperatura em tempo real
- **Gráficos Dinâmicos**: Visualização dos sinais vitais
- **Histórico Pessoal**: Últimas leituras e tendências
- **Status do Dispositivo**: Conectividade e bateria do ESP32

### 🚨 Sistema de Alertas
- **Detecção Automática**: Baseada em thresholds médicos
- **Classificação**: Normal, Elevado, Crítico
- **Localização GPS**: Coordenadas precisas para emergências
- **Contatos de Emergência**: Ligação direta para familiares
- **Integração SAMU**: Chamada automática para ambulância

## 🔧 Hardware - Circuito ECG

### Componentes
- **ESP32 DevKit** - Microcontrolador principal
- **AD620** - Amplificador de instrumentação
- **Eletrodos ECG** - Captação do sinal cardíaco
- **Resistores** - 10kΩ, 1MΩ para ganho
- **Capacitores** - Filtragem de ruído
- **Fonte 3.3V** - Alimentação estável

### Conexões
```
AD620 Pin 3 (V+) → ESP32 3.3V
AD620 Pin 4 (V-) → ESP32 GND  
AD620 Pin 6 (OUT) → ESP32 GPIO34 (ADC)
AD620 Pin 1,8 (RG) → Resistor 1MΩ (Ganho ~100)
```

### Código ESP32
```cpp
// Leitura do sinal ECG
int adcValue = analogRead(ecgPin);
float voltage = adcValue * (adcRef / adcRes);

// Detecção de batimentos
if (voltage > THRESHOLD && !beatDetected) {
    float bpm = 60000.0 / (currentTime - lastBeatTime);
    sendData(deviceId, (int)bpm, temperature);
}
```

## 📊 Banco de Dados

### Coleção `users`
```json
{
  "_id": ObjectId,
  "name": "Roberto Mendes",
  "device_id": "ESP32_006",
  "type": "patient",
  "age": 72,
  "condition": "Infarto Agudo",
  "current_bpm": 145,
  "current_temperature": 38.9,
  "location": {
    "lat": -23.5618,
    "lng": -46.6565,
    "address": "Av. Paulista, 1000"
  },
  "medications": ["Atenolol 50mg", "AAS 100mg"],
  "emergency_contact": "Esposa - (11) 98888-0072"
}
```

### Coleção `readings`
```json
{
  "_id": ObjectId,
  "device_id": "ESP32_006",
  "bpm": 145,
  "temperature": 38.9,
  "status": "critical",
  "timestamp": ISODate("2024-11-01T10:30:00Z")
}
```

## 🌐 Acesso ao Sistema

- **Interface Web**: http://127.0.0.1:8002
- **API Docs**: http://127.0.0.1:8002/docs
- **Dashboard**: http://127.0.0.1:8002/dashboard.html

## 🔒 Segurança

- **Validação de Dados**: Pydantic models
- **Sanitização**: Prevenção de SQL injection
- **CORS**: Configurado para desenvolvimento
- **Rate Limiting**: Proteção contra spam (futuro)
- **HTTPS**: Recomendado para produção

## 📈 Monitoramento e Alertas

### Thresholds Médicos
```python
# Normal: 60-100 BPM, 35.0-37.5°C
# Elevado: 50-120 BPM, 34.0-38.5°C  
# Crítico: <50 ou >120 BPM, <34.0 ou >38.5°C
```

### Tipos de Alerta
- 🟢 **Normal**: Sinais vitais dentro dos parâmetros
- 🟡 **Elevado**: Atenção necessária
- 🔴 **Crítico**: Emergência médica - localização ativada

## 🚀 Próximas Funcionalidades

- [ ] **Notificações Push** - Alertas em tempo real
- [ ] **Machine Learning** - Predição de eventos cardíacos
- [ ] **Telemedicina** - Videochamadas integradas
- [ ] **App Mobile** - Aplicativo nativo iOS/Android
- [ ] **Wearables** - Integração com smartwatches
- [ ] **Relatórios PDF** - Exportação de dados médicos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)
- Email: seu.email@exemplo.com

## 🙏 Agradecimentos

- **FastAPI** - Framework web excepcional
- **MongoDB** - Banco de dados flexível
- **ESP32** - Plataforma IoT robusta
- **Chart.js** - Visualizações incríveis
- **Comunidade Open Source** - Inspiração e suporte

---

**BioConnect** - Salvando vidas através da tecnologia 💙

![Footer](https://img.shields.io/badge/Made%20with-❤️-red) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)