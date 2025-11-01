#!/usr/bin/env python3
"""
Script de teste para verificar se o BioConnect está funcionando
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8002"

def test_api():
    print("🧪 Testando BioConnect API...")
    
    # Teste 1: Verificar se o servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Servidor está rodando")
        else:
            print("❌ Servidor não está respondendo")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor")
        print("   Execute: python app.py")
        return False
    
    # Teste 2: Login de médico
    try:
        login_data = {
            "email": "medico@teste.com",
            "password": "123456",
            "user_type": "doctor"
        }
        response = requests.post(f"{BASE_URL}/api/v1/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login de médico funcionando")
        else:
            print("❌ Erro no login de médico")
    except Exception as e:
        print(f"❌ Erro no teste de login: {e}")
    
    # Teste 3: Login de paciente
    try:
        login_data = {
            "email": "ESP32_001",
            "password": "",
            "user_type": "patient"
        }
        response = requests.post(f"{BASE_URL}/api/v1/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login de paciente funcionando")
        else:
            print("❌ Erro no login de paciente")
    except Exception as e:
        print(f"❌ Erro no teste de login de paciente: {e}")
    
    # Teste 4: Listar pacientes
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API de pacientes funcionando ({len(data.get('patients', []))} pacientes)")
        else:
            print("❌ Erro na API de pacientes")
    except Exception as e:
        print(f"❌ Erro no teste de pacientes: {e}")
    
    # Teste 5: Enviar dados ESP32
    try:
        esp32_data = {
            "device_id": "ESP32_001",
            "bpm": 75,
            "temperature": 36.8
        }
        response = requests.post(f"{BASE_URL}/api/v1/esp32/data", json=esp32_data)
        if response.status_code == 200:
            print("✅ API ESP32 funcionando")
        else:
            print("❌ Erro na API ESP32")
    except Exception as e:
        print(f"❌ Erro no teste ESP32: {e}")
    
    print("\n🎉 Testes concluídos!")
    print(f"🌐 Acesse: {BASE_URL}")
    return True

if __name__ == "__main__":
    test_api()