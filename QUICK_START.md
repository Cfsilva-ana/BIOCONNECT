# 🚀 BioConnect - Início Rápido

## ✅ Sistema Corrigido e Funcionando!

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar Sistema
```bash
python app.py
```

### 3. Acessar Interface
- **URL**: http://127.0.0.1:8002
- **API Docs**: http://127.0.0.1:8002/docs

### 4. Testar Sistema
```bash
python test_system.py
```

## 👨⚕️ Login de Teste

### Médico:
- **Email**: `medico@teste.com`
- **Senha**: `123456`

### Pacientes:
- **Device ID**: `ESP32_001` (João Silva)
- **Device ID**: `ESP32_002` (Maria Oliveira)
- **Device ID**: `ESP32_003` (Carlos Santos)
- **Device ID**: `ESP32_004` (Ana Costa)
- **Device ID**: `ESP32_005` (Pedro Lima)

## 🔌 API ESP32

### Enviar Dados:
```bash
curl -X POST "http://127.0.0.1:8002/api/v1/esp32/data" \
     -H "Content-Type: application/json" \
     -d '{
       "device_id": "ESP32_001",
       "bpm": 72,
       "temperature": 36.5
     }'
```

### Verificar Status:
```bash
curl "http://127.0.0.1:8002/api/v1/esp32/status/ESP32_001"
```

## ✨ Funcionalidades

- ✅ Interface web completa
- ✅ Login médico/paciente
- ✅ Dashboard em tempo real
- ✅ API para ESP32
- ✅ Banco MongoDB
- ✅ Dados de teste
- ✅ Sistema de alertas

## 🛠️ Problemas Corrigidos

- ✅ Código incompleto
- ✅ Variáveis indefinidas
- ✅ Erros de sintaxe
- ✅ Funções faltando
- ✅ Interface HTML
- ✅ Dependências
- ✅ Lifespan events

**Sistema 100% funcional!** 🎉