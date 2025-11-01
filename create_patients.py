import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB connection
MONGO_URL = "mongodb+srv://bioconnect_user:Bio2050@bioconnect.jk9t70o.mongodb.net/?appName=BioConnect"

async def create_patients():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.bioconnect
    users_collection = db.users
    readings_collection = db.readings
    
    # Criar médico de teste
    doctor = {
        "name": "Dr. João Médico",
        "email": "medico@teste.com",
        "password": "123456",
        "type": "doctor",
        "created_at": datetime.utcnow()
    }
    await users_collection.insert_one(doctor)
    
    # Criar pacientes de teste
    patients = [
        {
            "name": "Roberto Mendes",
            "device_id": "ESP32_006",
            "type": "patient",
            "age": 72,
            "gender": "Masculino",
            "condition": "Infarto Agudo",
            "blood_type": "A+",
            "allergies": "Penicilina, Aspirina",
            "medications": ["Atenolol 50mg", "AAS 100mg", "Losartana 50mg", "Sinvastatina 20mg"],
            "phone": "(11) 99999-0072",
            "email": "roberto.mendes@email.com",
            "address": "Av. Paulista, 1000 - Bela Vista, São Paulo, SP",
            "emergency_contact": "Esposa - Maria Mendes (11) 98888-0072",
            "doctor_notes": "PACIENTE CRÍTICO - Histórico de infarto agudo do miocárdio. Apresenta taquicardia e hipertermia. Monitoramento contínuo necessário.",
            "current_bpm": 145,
            "current_temperature": 38.9,
            "location": {
                "lat": -23.5618,
                "lng": -46.6565,
                "address": "Av. Paulista, 1000 - Bela Vista, São Paulo, SP"
            },
            "created_at": datetime.utcnow()
        },
        {
            "name": "João Silva",
            "device_id": "ESP32_001",
            "type": "patient",
            "age": 45,
            "gender": "Masculino",
            "condition": "Hipertensão",
            "blood_type": "O+",
            "allergies": "Nenhuma",
            "medications": ["Losartana 25mg", "Hidroclorotiazida 12.5mg"],
            "phone": "(11) 99999-0001",
            "email": "joao.silva@email.com",
            "address": "Rua das Flores, 123 - São Paulo, SP",
            "emergency_contact": "Esposa - Ana Silva (11) 98888-0001",
            "doctor_notes": "Paciente com hipertensão controlada. Acompanhamento regular.",
            "current_bpm": 85,
            "current_temperature": 36.8,
            "location": {
                "lat": -23.5505,
                "lng": -46.6333,
                "address": "Rua das Flores, 123 - São Paulo, SP"
            },
            "created_at": datetime.utcnow()
        },
        {
            "name": "Maria Oliveira",
            "device_id": "ESP32_002",
            "type": "patient",
            "age": 32,
            "gender": "Feminino",
            "condition": "Diabetes Tipo 2",
            "blood_type": "A+",
            "allergies": "Penicilina",
            "medications": ["Metformina 850mg", "Insulina NPH"],
            "phone": "(11) 99999-5678",
            "email": "maria.oliveira@email.com",
            "address": "Av. Paulista, 456 - São Paulo, SP",
            "emergency_contact": "Carlos Oliveira - (11) 88888-5678",
            "doctor_notes": "Diabetes bem controlada. Manter dieta e exercícios.",
            "current_bpm": 72,
            "current_temperature": 36.5,
            "admission_date": "2024-01-08",
            "location": {
                "lat": -23.5489,
                "lng": -46.6388,
                "address": "Av. Paulista, 456 - São Paulo, SP"
            },
            "created_at": datetime.utcnow()
        },
        {
            "name": "Carlos Santos",
            "device_id": "ESP32_003",
            "type": "patient",
            "age": 58,
            "gender": "Masculino",
            "condition": "Arritmia",
            "blood_type": "B+",
            "allergies": "Penicilina",
            "medications": ["Amiodarona 200mg", "Varfarina 5mg"],
            "phone": "(11) 99999-0003",
            "email": "carlos.santos@email.com",
            "address": "Rua Augusta, 789 - São Paulo, SP",
            "emergency_contact": "Filho - Pedro Santos (11) 98888-0003",
            "doctor_notes": "Fibrilação atrial. Anticoagulação em uso. Monitorar INR.",
            "current_bpm": 95,
            "current_temperature": 37.2,
            "location": {
                "lat": -23.5558,
                "lng": -46.6396,
                "address": "Rua Augusta, 789 - São Paulo, SP"
            },
            "created_at": datetime.utcnow()
        },
        {
            "name": "Ana Costa",
            "device_id": "ESP32_004",
            "type": "patient",
            "age": 28,
            "gender": "Feminino",
            "condition": "Saudável",
            "blood_type": "AB+",
            "allergies": "Nenhuma",
            "medications": ["Vitamina D", "Ácido Fólico"],
            "phone": "(11) 99999-0004",
            "email": "ana.costa@email.com",
            "address": "Rua da Consolação, 321 - São Paulo, SP",
            "emergency_contact": "Marido - Luis Costa (11) 98888-0004",
            "doctor_notes": "Paciente saudável. Acompanhamento preventivo.",
            "current_bpm": 68,
            "current_temperature": 36.4,
            "location": {
                "lat": -23.5431,
                "lng": -46.6291,
                "address": "Rua da Consolação, 321 - São Paulo, SP"
            },
            "created_at": datetime.utcnow()
        },
        {
            "name": "Pedro Lima",
            "device_id": "ESP32_005",
            "type": "patient",
            "age": 67,
            "gender": "Masculino",
            "condition": "Cardiopatia",
            "blood_type": "O-",
            "allergies": "Aspirina",
            "medications": ["Carvedilol 25mg", "Enalapril 10mg", "Furosemida 40mg"],
            "phone": "(11) 99999-0005",
            "email": "pedro.lima@email.com",
            "address": "Av. Ipiranga, 654 - São Paulo, SP",
            "emergency_contact": "Filha - Carla Lima (11) 98888-0005",
            "doctor_notes": "Insuficiência cardíaca compensada. Controle rigoroso de peso e diurese.",
            "current_bpm": 78,
            "current_temperature": 36.7,
            "location": {
                "lat": -23.5435,
                "lng": -46.6477,
                "address": "Av. Ipiranga, 654 - São Paulo, SP"
            },
            "created_at": datetime.utcnow()
        }
    ]
    
    await users_collection.insert_many(patients)
    
    # Criar leituras de teste
    test_readings = [
        {
            "device_id": "ESP32_006",
            "bpm": 145,
            "temperature": 38.9,
            "status": "critical",
            "timestamp": datetime.utcnow()
        },
        {
            "device_id": "ESP32_001",
            "bpm": 85,
            "temperature": 36.8,
            "status": "elevated",
            "timestamp": datetime.utcnow()
        },
        {
            "device_id": "ESP32_002",
            "bpm": 72,
            "temperature": 36.5,
            "status": "normal",
            "timestamp": datetime.utcnow()
        },
        {
            "device_id": "ESP32_003",
            "bpm": 95,
            "temperature": 37.2,
            "status": "elevated",
            "timestamp": datetime.utcnow()
        },
        {
            "device_id": "ESP32_004",
            "bpm": 68,
            "temperature": 36.4,
            "status": "normal",
            "timestamp": datetime.utcnow()
        },
        {
            "device_id": "ESP32_005",
            "bpm": 78,
            "temperature": 36.7,
            "status": "normal",
            "timestamp": datetime.utcnow()
        }
    ]
    
    await readings_collection.insert_many(test_readings)
    
    print("Pacientes criados no MongoDB Atlas!")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_patients())