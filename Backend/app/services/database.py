from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB]
        self.readings = self.db["readings"]
        self.alerts = self.db["alerts"]
        self.devices = self.db["devices"]
        
        # Criar índices para performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Criar índices para otimizar consultas"""
        try:
            self.readings.create_index([("patient_id", 1), ("timestamp", -1)])
            self.readings.create_index([("device_id", 1), ("timestamp", -1)])
            self.alerts.create_index([("patient_id", 1), ("timestamp", -1)])
            self.devices.create_index("device_id", unique=True)
        except Exception as e:
            logger.warning(f"Erro ao criar índices: {e}")
    
    def save_reading(self, reading_data: dict, patient_id: str) -> str:
        """Salvar leitura biomédica"""
        reading_data.update({
            "patient_id": patient_id,
            "timestamp": datetime.utcnow(),
            "created_at": datetime.utcnow()
        })
        result = self.readings.insert_one(reading_data)
        return str(result.inserted_id)
    
    def get_patient_readings(self, patient_id: str, limit: int = 100) -> List[dict]:
        """Buscar leituras de um paciente"""
        cursor = self.readings.find({"patient_id": patient_id}).sort("timestamp", -1).limit(limit)
        readings = []
        for reading in cursor:
            reading["id"] = str(reading["_id"])
            del reading["_id"]
            readings.append(reading)
        return readings
    
    def get_device_readings(self, device_id: str, limit: int = 100) -> List[dict]:
        """Buscar leituras de um dispositivo"""
        cursor = self.readings.find({"device_id": device_id}).sort("timestamp", -1).limit(limit)
        readings = []
        for reading in cursor:
            reading["id"] = str(reading["_id"])
            del reading["_id"]
            readings.append(reading)
        return readings
    
    def save_alert(self, alert_data: dict) -> str:
        """Salvar alerta"""
        alert_data.update({
            "timestamp": datetime.utcnow(),
            "resolved": False
        })
        result = self.alerts.insert_one(alert_data)
        return str(result.inserted_id)
    
    def get_patient_alerts(self, patient_id: str, limit: int = 50) -> List[dict]:
        """Buscar alertas de um paciente"""
        cursor = self.alerts.find({"patient_id": patient_id}).sort("timestamp", -1).limit(limit)
        alerts = []
        for alert in cursor:
            alert["id"] = str(alert["_id"])
            del alert["_id"]
            alerts.append(alert)
        return alerts
    
    def update_device_status(self, device_id: str, patient_id: str):
        """Atualizar status do dispositivo"""
        self.devices.update_one(
            {"device_id": device_id},
            {
                "$set": {
                    "patient_id": patient_id,
                    "last_reading": datetime.utcnow(),
                    "status": "active"
                },
                "$inc": {"total_readings": 1}
            },
            upsert=True
        )
    
    def get_devices(self) -> List[dict]:
        """Listar todos os dispositivos"""
        devices = []
        for device in self.devices.find():
            device["id"] = str(device["_id"])
            del device["_id"]
            devices.append(device)
        return devices
    
    def get_reading_statistics(self, patient_id: str) -> dict:
        """Calcular estatísticas das leituras"""
        pipeline = [
            {"$match": {"patient_id": patient_id}},
            {"$group": {
                "_id": None,
                "avg_heart_rate": {"$avg": "$heart_rate"},
                "avg_temperature": {"$avg": "$temperature"},
                "min_heart_rate": {"$min": "$heart_rate"},
                "max_heart_rate": {"$max": "$heart_rate"},
                "min_temperature": {"$min": "$temperature"},
                "max_temperature": {"$max": "$temperature"},
                "total_readings": {"$sum": 1}
            }}
        ]
        
        result = list(self.readings.aggregate(pipeline))
        if result:
            stats = result[0]
            del stats["_id"]
            return stats
        return {}

# Instância global do serviço de banco
db_service = DatabaseService()