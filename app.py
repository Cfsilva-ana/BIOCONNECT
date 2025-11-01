from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio
from contextlib import asynccontextmanager

# MongoDB connection
MONGO_URL = "mongodb+srv://bioconnect_user:Bio2050@bioconnect.jk9t70o.mongodb.net/?appName=BioConnect"
client = None
db = None
users_collection = None
readings_collection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global client, db, users_collection, readings_collection
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.bioconnect
    users_collection = db.users
    readings_collection = db.readings
    await init_db()
    yield
    # Shutdown
    if client:
        client.close()

app = FastAPI(
    title="BioConnect", 
    description="Plataforma de Monitoramento Biomédico",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



class LoginRequest(BaseModel):
    email: str
    password: str
    user_type: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    user_type: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>BioConnect</h1><p>Sistema de monitoramento biomédico em desenvolvimento...</p>")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard</h1><p>Em desenvolvimento...</p>")

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Profile</h1><p>Em desenvolvimento...</p>")

@app.get("/dashboard.html", response_class=HTMLResponse)
async def dashboard_html(request: Request):
    try:
        with open("templates/dashboard.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard</h1><p>Arquivo não encontrado...</p>")

@app.post("/api/v1/login")
async def login(request: LoginRequest):
    if request.user_type == "patient":
        user = await users_collection.find_one({"device_id": request.email, "type": "patient"})
        if user:
            return {
                "status": "success",
                "user": {
                    "id": str(user["_id"]),
                    "name": user["name"],
                    "email": request.email,
                    "type": "patient"
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Device ID não encontrado")
    else:
        user = await users_collection.find_one({"email": request.email, "password": request.password, "type": "doctor"})
        if user:
            return {
                "status": "success",
                "user": {
                    "id": str(user["_id"]),
                    "name": user["name"],
                    "email": request.email,
                    "type": "doctor"
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Email ou senha inválidos")

@app.post("/api/v1/register")
async def register(request: RegisterRequest):
    if request.user_type == "patient":
        existing = await users_collection.find_one({"device_id": request.email})
        if existing:
            raise HTTPException(status_code=400, detail="Device ID já cadastrado")
        
        await users_collection.insert_one({
            "name": request.name,
            "device_id": request.email,
            "type": "patient",
            "created_at": datetime.utcnow()
        })
    else:
        existing = await users_collection.find_one({"email": request.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        await users_collection.insert_one({
            "name": request.name,
            "email": request.email,
            "password": request.password,
            "type": "doctor",
            "created_at": datetime.utcnow()
        })
    
    return {
        "status": "success",
        "message": "Usuário cadastrado com sucesso"
    }

@app.get("/api/v1/readings/{device_id}")
async def get_patient_readings(device_id: str):
    """Obter leituras de um paciente específico"""
    try:
        readings = await readings_collection.find({"device_id": device_id}).sort("timestamp", -1).limit(20).to_list(20)
        # Convert ObjectId to string for JSON serialization
        for reading in readings:
            if '_id' in reading:
                reading['_id'] = str(reading['_id'])
            if 'timestamp' in reading and hasattr(reading['timestamp'], 'isoformat'):
                reading['timestamp'] = reading['timestamp'].isoformat()
        return {"readings": readings}
    except Exception as e:
        print(f"Error in get_patient_readings: {e}")
        return {"readings": []}

@app.get("/api/v1/readings")
async def get_readings():
    try:
        readings = await readings_collection.find().sort("timestamp", -1).limit(10).to_list(10)
        # Convert ObjectId to string for JSON serialization
        for reading in readings:
            if '_id' in reading:
                reading['_id'] = str(reading['_id'])
            if 'timestamp' in reading and hasattr(reading['timestamp'], 'isoformat'):
                reading['timestamp'] = reading['timestamp'].isoformat()
        return {"readings": readings}
    except Exception as e:
        print(f"Error in get_readings: {e}")
        # Return sample data if MongoDB fails
        return {
            "readings": [
                {"bpm": 72, "temperature": 36.5, "timestamp": "2024-01-15T10:00:00", "status": "normal"},
                {"bpm": 75, "temperature": 36.8, "timestamp": "2024-01-15T10:05:00", "status": "normal"},
                {"bpm": 70, "temperature": 36.3, "timestamp": "2024-01-15T10:10:00", "status": "normal"}
            ]
        }

@app.get("/api/v1/patients")
async def get_patients():
    patients = []
    async for user in users_collection.find({"type": "patient"}):
        # Pegar última leitura do paciente
        last_reading = await readings_collection.find_one({"device_id": user["device_id"]}, sort=[("timestamp", -1)])
        total_readings = await readings_collection.count_documents({"device_id": user["device_id"]})
        
        if not last_reading:
            last_reading = {"bpm": 0, "temperature": 0, "timestamp": "N/A", "status": "offline"}
        
        patients.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "device_id": user["device_id"],
            "age": user.get("age", 0),
            "condition": user.get("condition", "N/A"),
            "status": "online" if total_readings > 0 else "offline",
            "last_reading": last_reading["timestamp"],
            "bpm": last_reading["bpm"],
            "temperature": last_reading["temperature"],
            "vital_status": last_reading["status"],
            "total_readings": total_readings
        })
    return {"patients": patients}

@app.get("/api/v1/patients/{patient_id}/history")
async def get_patient_history(patient_id: str):
    try:
        readings = await readings_collection.find({"device_id": patient_id}).sort("timestamp", -1).to_list(100)
        # Convert ObjectId to string for JSON serialization
        for reading in readings:
            if '_id' in reading:
                reading['_id'] = str(reading['_id'])
            if 'timestamp' in reading and hasattr(reading['timestamp'], 'isoformat'):
                reading['timestamp'] = reading['timestamp'].isoformat()
        return {"patient_id": patient_id, "readings": readings}
    except Exception as e:
        print(f"Error in get_patient_history: {e}")
        return {"patient_id": patient_id, "readings": []}

@app.get("/api/v1/patients/{patient_id}/details")
async def get_patient_details(patient_id: str):
    from bson import ObjectId
    try:
        patient = await users_collection.find_one({"_id": ObjectId(patient_id)})
    except:
        patient = await users_collection.find_one({"device_id": patient_id})
    
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    readings = await readings_collection.find({"device_id": patient["device_id"]}).to_list(1000)
    last_reading = readings[-1] if readings else None
    
    return {
        "id": str(patient["_id"]),
        "name": patient["name"],
        "device_id": patient["device_id"],
        "age": patient.get("age", 0),
        "condition": patient.get("condition", "N/A"),
        "last_reading": last_reading,
        "total_readings": len(readings)
    }

class ESP32Data(BaseModel):
    device_id: str
    bpm: int
    temperature: float

@app.post("/api/v1/esp32/data")
async def receive_esp32_data(data: ESP32Data):
    """Receber dados do ESP32"""
    try:
        # Determinar status baseado nos valores
        status = "normal"
        if data.bpm < 60 or data.bpm > 100:
            status = "elevated"
        if data.temperature < 35.0 or data.temperature > 37.5:
            status = "elevated"
        if data.bpm < 50 or data.bpm > 120 or data.temperature < 34.0 or data.temperature > 38.5:
            status = "critical"
        
        # Salvar no banco
        reading = {
            "device_id": data.device_id,
            "bpm": data.bpm,
            "temperature": data.temperature,
            "status": status,
            "timestamp": datetime.utcnow()
        }
        
        await readings_collection.insert_one(reading)
        
        return {
            "status": "success",
            "message": "Dados recebidos com sucesso",
            "vital_status": status
        }
    except Exception as e:
        print(f"Error saving ESP32 data: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar dados")

@app.get("/api/v1/esp32/status/{device_id}")
async def get_esp32_status(device_id: str):
    """Verificar status do dispositivo ESP32"""
    try:
        last_reading = await readings_collection.find_one(
            {"device_id": device_id}, 
            sort=[("timestamp", -1)]
        )
        
        if not last_reading:
            return {"status": "offline", "message": "Nenhuma leitura encontrada"}
        
        # Verificar se a última leitura foi há menos de 5 minutos
        time_diff = datetime.utcnow() - last_reading["timestamp"]
        is_online = time_diff.total_seconds() < 300  # 5 minutos
        
        return {
            "status": "online" if is_online else "offline",
            "last_reading": last_reading["timestamp"].isoformat(),
            "bpm": last_reading["bpm"],
            "temperature": last_reading["temperature"],
            "vital_status": last_reading["status"]
        }
    except Exception as e:
        print(f"Error getting ESP32 status: {e}")
        return {"status": "error", "message": "Erro ao verificar status"}

async def init_db():
    """Inicializar banco de dados com dados de teste"""
    try:
        # Verificar se já existem usuários
        existing_users = await users_collection.count_documents({})
        if existing_users > 0:
            print("Database already initialized")
            return
        
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
                "name": "João Silva",
                "device_id": "ESP32_001",
                "type": "patient",
                "age": 45,
                "condition": "Hipertensão",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Maria Oliveira",
                "device_id": "ESP32_002",
                "type": "patient",
                "age": 32,
                "condition": "Diabetes",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Carlos Santos",
                "device_id": "ESP32_003",
                "type": "patient",
                "age": 58,
                "condition": "Arritmia",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Ana Costa",
                "device_id": "ESP32_004",
                "type": "patient",
                "age": 28,
                "condition": "Saudável",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Pedro Lima",
                "device_id": "ESP32_005",
                "type": "patient",
                "age": 67,
                "condition": "Cardiopatia",
                "created_at": datetime.utcnow()
            }
        ]
        
        await users_collection.insert_many(patients)
        
        # Criar algumas leituras de teste
        test_readings = [
            {
                "device_id": "ESP32_001",
                "bpm": 72,
                "temperature": 36.5,
                "status": "normal",
                "timestamp": datetime.utcnow()
            },
            {
                "device_id": "ESP32_002",
                "bpm": 68,
                "temperature": 36.8,
                "status": "normal",
                "timestamp": datetime.utcnow()
            },
            {
                "device_id": "ESP32_003",
                "bpm": 105,
                "temperature": 37.2,
                "status": "elevated",
                "timestamp": datetime.utcnow()
            }
        ]
        
        await readings_collection.insert_many(test_readings)
        print("Database initialized with test data")
        
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    print("Iniciando BioConnect...")
    print("Conectando ao MongoDB...")
    print("Acesse: http://127.0.0.1:8002")
    uvicorn.run(app, host="127.0.0.1", port=8002)