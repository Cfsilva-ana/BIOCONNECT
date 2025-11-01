# 🏥 BIOCONNECT 2050 - Sistema de Monitoramento Biomédico

## 📋 O que é o BIOCONNECT 2050?

O BIOCONNECT 2050 é um sistema completo de monitoramento biomédico que conecta dispositivos IoT (como ESP32) a uma plataforma web para acompanhamento em tempo real de sinais vitais.

### 🎯 Objetivo Principal
Permitir que dispositivos ESP32 equipados com sensores enviem dados de **frequência cardíaca** e **temperatura corporal** para um servidor, onde são:
- ✅ Armazenados no banco de dados
- ✅ Analisados automaticamente
- ✅ Convertidos em alertas quando necessário
- ✅ Disponibilizados para consulta via API

### 🔧 Como Funciona
1. **ESP32** coleta dados dos sensores
2. **Envia via WiFi** para nossa API
3. **Backend processa** e salva no MongoDB
4. **Sistema gera alertas** automáticos
5. **Frontend/App** consulta os dados

## 🏗️ Estrutura do Projeto

```
BIOCONNECT/Backend/
├── app/                     # 📁 Código principal da aplicação
│   ├── api/                 # 🌐 Endpoints da API REST
│   │   ├── readings.py      # 📊 Receber/consultar leituras
│   │   └── devices.py       # 📱 Gerenciar dispositivos
│   ├── core/
│   │   └── config.py        # ⚙️ Configurações do sistema
│   ├── models/
│   │   └── schemas.py       # 📝 Estrutura dos dados
│   ├── services/
│   │   ├── database.py      # 🗄️ Operações no MongoDB
│   │   └── alert_service.py # 🚨 Lógica de alertas
│   └── main.py              # 🚀 Arquivo principal
├── env/
│   └── .env                 # 🔐 Credenciais e configurações
├── requirements.txt         # 📦 Dependências Python
└── README.md               # 📖 Esta documentação
```

## 🚀 Como Instalar e Usar

### Pré-requisitos
- ✅ Python 3.8 ou superior instalado
- ✅ Conexão com internet
- ✅ Conta no MongoDB Atlas (gratuita)

### Passo 1: Instalar Dependências

Abra o terminal na pasta `Backend/` e execute:

```bash
pip install -r requirements.txt
```

**O que isso faz?** Instala todas as bibliotecas necessárias:
- `fastapi`: Framework web moderno e rápido
- `pymongo`: Conecta com MongoDB
- `pydantic`: Validação automática de dados
- `uvicorn`: Servidor web para rodar a API

### Passo 2: Configurar Banco de Dados

O arquivo `env/.env` já está configurado com um banco MongoDB gratuito:

```env
MONGO_URI=mongodb+srv://bioconnect_user:Bio2050@bioconnect.jk9t70o.mongodb.net/?appName=BioConnect
MONGO_DB=bioconnect2050
```

**Quer usar seu próprio banco?** 
1. Crie uma conta gratuita em [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Crie um cluster
3. Substitua a `MONGO_URI` no arquivo `.env`

### Passo 3: Executar o Servidor

```bash
python -m app.main
```

**Pronto!** Sua API estará rodando em: http://127.0.0.1:3000

### Passo 4: Testar se Funcionou

Abra seu navegador e acesse:
- **Página inicial**: http://127.0.0.1:3000
- **Documentação**: http://127.0.0.1:3000/docs
- **Status**: http://127.0.0.1:3000/health

## 📡 Como Usar a API

### 🎮 Documentação Interativa (Recomendado)

Acesse http://127.0.0.1:3000/docs para uma interface visual onde você pode:
- ✅ Ver todos os endpoints disponíveis
- ✅ Testar diretamente no navegador
- ✅ Ver exemplos de requisições e respostas

### 📊 Principais Funcionalidades

#### 1. 📤 Enviar Dados do ESP32

**Endpoint**: `POST /api/v1/readings`

**Para que serve**: Receber dados dos sensores do ESP32

**Como usar no ESP32**:
```cpp
// Código Arduino/ESP32
HTTPClient http;
http.begin("http://192.168.1.100:3000/api/v1/readings");
http.addHeader("Content-Type", "application/json");

String json = "{\"device_id\":\"ESP32_01\",\"heart_rate\":" + String(bpm) + ",\"temperature\":" + String(temp) + "}";
int httpCode = http.POST(json);
```

**Exemplo de dados**:
```json
{
  "device_id": "ESP32_01",
  "heart_rate": 85,
  "temperature": 36.8
}
```

**O que acontece**:
- ✅ Dados são salvos no banco
- ✅ Sistema verifica se há alertas
- ✅ Retorna confirmação + alertas (se houver)

#### 2. 📈 Consultar Histórico

**Endpoint**: `GET /api/v1/readings/device/ESP32_01`

**Para que serve**: Ver todas as leituras de um dispositivo

**Retorna**:
- Lista das últimas 100 leituras
- Estatísticas (média, mínimo, máximo)
- Total de leituras registradas

#### 3. 🚨 Ver Alertas

**Endpoint**: `GET /api/v1/readings/patient/ESP32_01/alerts`

**Para que serve**: Consultar alertas médicos gerados

#### 4. 📱 Status dos Dispositivos

**Endpoint**: `GET /api/v1/devices`

**Para que serve**: Ver quais ESP32 estão conectados e ativos

## 🚨 Sistema de Alertas Automáticos

### Como Funciona

Toda vez que o ESP32 envia dados, o sistema **automaticamente verifica** se os valores estão dentro dos limites normais. Se não estiverem, **gera alertas instantâneos**.

### 📊 Limites Médicos Configurados

| 🫀 **Frequência Cardíaca** | Valor | 🚨 Alerta |
|---------------------------|-------|----------|
| **Normal** | 50 - 120 bpm | ✅ Nenhum |
| **Muito Alta (Taquicardia)** | > 120 bpm | 🔴 **CRÍTICO** |
| **Muito Baixa (Bradicardia)** | < 50 bpm | 🟡 **ATENÇÃO** |

| 🌡️ **Temperatura Corporal** | Valor | 🚨 Alerta |
|----------------------------|-------|----------|
| **Normal** | ≤ 37.5°C | ✅ Nenhum |
| **Febre** | > 37.5°C | 🟡 **ATENÇÃO** |

### 📱 Exemplo Prático

**Cenário**: ESP32 envia dados com frequência cardíaca de 130 bpm

**O que acontece**:
1. ✅ Dados são salvos normalmente
2. 🚨 Sistema detecta: 130 > 120 (limite)
3. 📝 Cria alerta: "Frequência cardíaca elevada: 130 bpm"
4. 📤 Retorna resposta com o alerta
5. 💾 Salva alerta no banco para consulta posterior

### 🔧 Personalizar Limites

Para alterar os limites, edite o arquivo `app/core/config.py`:

```python
# Configurações de alertas
HEART_RATE_HIGH: int = 120    # Altere aqui
HEART_RATE_LOW: int = 50      # Altere aqui  
TEMPERATURE_HIGH: float = 37.5 # Altere aqui
```

## 🗄️ Como os Dados são Armazenados

### 📊 Estrutura do Banco MongoDB

O sistema usa **3 coleções principais** no MongoDB:

#### 1. 📈 `readings` - Leituras dos Sensores
**O que armazena**: Cada medição enviada pelo ESP32

```json
{
  "device_id": "ESP32_01",           // Qual ESP32 enviou
  "patient_id": "ESP32_01",          // Paciente associado
  "heart_rate": 85,                  // BPM medido
  "temperature": 36.8,               // Temperatura em °C
  "timestamp": "2024-01-15T10:30:00Z", // Quando foi medido
  "alerts": ["Temperatura elevada: 37.8°C"] // Alertas gerados
}
```

#### 2. 🚨 `alerts` - Alertas Médicos
**O que armazena**: Todos os alertas gerados pelo sistema

```json
{
  "patient_id": "ESP32_01",
  "device_id": "ESP32_01",
  "alert_type": "temperature_high",    // Tipo do alerta
  "message": "Temperatura elevada: 37.8°C", // Mensagem legível
  "value": 37.8,                      // Valor que causou o alerta
  "severity": "medium",               // Gravidade (low/medium/high)
  "timestamp": "2024-01-15T10:30:00Z",
  "resolved": false                   // Se foi resolvido
}
```

#### 3. 📱 `devices` - Status dos Dispositivos
**O que armazena**: Informações sobre cada ESP32

```json
{
  "device_id": "ESP32_01",
  "patient_id": "ESP32_01",
  "status": "active",                 // online/offline/active
  "last_reading": "2024-01-15T10:30:00Z", // Última vez que enviou dados
  "total_readings": 1250              // Total de leituras enviadas
}
```

### 🔍 Consultas Otimizadas

O sistema cria **índices automáticos** para consultas rápidas:
- ✅ Buscar por dispositivo + data
- ✅ Buscar por paciente + data  
- ✅ Listar alertas recentes
- ✅ Verificar status dos dispositivos

## 🔧 Configurações Avançadas

### Personalizar Limites de Alertas

Edite `app/core/config.py`:

```python
HEART_RATE_HIGH: int = 120
HEART_RATE_LOW: int = 50
TEMPERATURE_HIGH: float = 37.5
```

### Logging

Logs são salvos automaticamente com níveis:
- INFO: Operações normais
- WARNING: Situações de atenção
- ERROR: Erros do sistema

## 🧪 Testando o Sistema

### 🎯 Método 1: Interface Visual (Mais Fácil)

1. **Abra**: http://127.0.0.1:3000/docs
2. **Clique** em `POST /api/v1/readings`
3. **Clique** em "Try it out"
4. **Cole** este exemplo:
   ```json
   {
     "device_id": "ESP32_TESTE",
     "heart_rate": 130,
     "temperature": 38.0
   }
   ```
5. **Clique** em "Execute"
6. **Veja** a resposta com alertas gerados!

### 💻 Método 2: Linha de Comando

**Enviar dados (simula ESP32)**:
```bash
curl -X POST "http://127.0.0.1:3000/api/v1/readings" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "ESP32_01",
    "heart_rate": 95,
    "temperature": 36.5
  }'
```

**Consultar histórico**:
```bash
curl "http://127.0.0.1:3000/api/v1/readings/device/ESP32_01"
```

### 🐍 Método 3: Script Python

```python
import requests
import time

# Simular ESP32 enviando dados
def simular_esp32():
    url = "http://127.0.0.1:3000/api/v1/readings"
    
    # Dados normais
    dados_normais = {
        "device_id": "ESP32_SIMULADO",
        "heart_rate": 75,
        "temperature": 36.5
    }
    
    # Dados com alerta
    dados_alerta = {
        "device_id": "ESP32_SIMULADO", 
        "heart_rate": 130,  # Vai gerar alerta!
        "temperature": 38.2  # Vai gerar alerta!
    }
    
    print("📤 Enviando dados normais...")
    response = requests.post(url, json=dados_normais)
    print(f"✅ Resposta: {response.json()}")
    
    time.sleep(2)
    
    print("\n📤 Enviando dados com alertas...")
    response = requests.post(url, json=dados_alerta)
    print(f"🚨 Resposta: {response.json()}")

if __name__ == "__main__":
    simular_esp32()
```

### 🎮 Testes Sugeridos

1. **Teste Normal**: BPM=75, Temp=36.5 (sem alertas)
2. **Teste Taquicardia**: BPM=130, Temp=36.5 (alerta cardíaco)
3. **Teste Febre**: BPM=75, Temp=38.0 (alerta temperatura)
4. **Teste Crítico**: BPM=140, Temp=39.0 (múltiplos alertas)

## 🚀 Próximos Passos

### 🔧 Para Desenvolvedores ESP32

1. **Configure seu ESP32** para enviar dados para:
   ```
   URL: http://SEU_IP:3000/api/v1/readings
   Método: POST
   Content-Type: application/json
   ```

2. **Exemplo de código ESP32**:
   ```cpp
   #include <WiFi.h>
   #include <HTTPClient.h>
   
   void enviarDados(int bpm, float temp) {
     HTTPClient http;
     http.begin("http://192.168.1.100:3000/api/v1/readings");
     http.addHeader("Content-Type", "application/json");
     
     String json = "{\"device_id\":\"" + WiFi.macAddress() + 
                   "\",\"heart_rate\":" + String(bpm) + 
                   ",\"temperature\":" + String(temp) + "}";
     
     int codigo = http.POST(json);
     if (codigo == 200) {
       Serial.println("✅ Dados enviados!");
     }
     http.end();
   }
   ```

### 📱 Para Desenvolvedores Frontend

**Endpoints principais para seu app/site**:
- `GET /api/v1/readings/device/{id}` - Histórico
- `GET /api/v1/readings/patient/{id}/alerts` - Alertas
- `GET /api/v1/devices` - Lista de dispositivos

### 🏥 Para Profissionais de Saúde

- **Acesse**: http://127.0.0.1:3000/docs
- **Monitore** pacientes em tempo real
- **Configure** limites personalizados
- **Exporte** dados para análise

## ❓ Problemas Comuns

### 🔴 "Erro de conexão com MongoDB"
**Solução**: Verifique se o arquivo `env/.env` está correto

### 🔴 "ModuleNotFoundError"
**Solução**: Execute `pip install -r requirements.txt`

### 🔴 "Porta 3000 ocupada"
**Solução**: Altere a porta no arquivo `app/main.py` (linha final)

### 🔴 ESP32 não consegue enviar dados
**Soluções**:
- ✅ Verifique se o ESP32 está na mesma rede WiFi
- ✅ Use o IP correto do computador (não localhost)
- ✅ Desative firewall temporariamente para teste

## 📞 Suporte e Contato

**Documentação completa**: http://127.0.0.1:3000/docs
**Status do sistema**: http://127.0.0.1:3000/health

### 🛠️ Para Desenvolvedores
- Logs detalhados aparecem no terminal
- Use `/health` para verificar conectividade
- Consulte `/docs` para testar endpoints

---

## 🎉 Parabéns!

Você agora tem um **sistema completo de monitoramento biomédico** funcionando!

**O que você conseguiu**:
- ✅ API REST profissional
- ✅ Banco de dados na nuvem
- ✅ Sistema de alertas automático
- ✅ Documentação interativa
- ✅ Pronto para ESP32 e frontend

**BIOCONNECT 2050** - Conectando tecnologia e saúde! 🏥💙🚀