from typing import List, Dict
from datetime import datetime
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AlertService:
    """Serviço para processamento de alertas biomédicos"""
    
    @staticmethod
    def process_reading_alerts(reading: Dict, patient_id: str) -> List[Dict]:
        """Processar alertas baseados na leitura"""
        alerts = []
        
        # Verificar frequência cardíaca
        heart_rate = reading.get("heart_rate")
        if heart_rate:
            if heart_rate > settings.HEART_RATE_HIGH:
                alerts.append({
                    "patient_id": patient_id,
                    "device_id": reading["device_id"],
                    "alert_type": "heart_rate_high",
                    "message": f"Frequência cardíaca elevada: {heart_rate} bpm",
                    "value": heart_rate,
                    "severity": "high"
                })
            elif heart_rate < settings.HEART_RATE_LOW:
                alerts.append({
                    "patient_id": patient_id,
                    "device_id": reading["device_id"],
                    "alert_type": "heart_rate_low",
                    "message": f"Frequência cardíaca baixa: {heart_rate} bpm",
                    "value": heart_rate,
                    "severity": "medium"
                })
        
        # Verificar temperatura
        temperature = reading.get("temperature")
        if temperature and temperature > settings.TEMPERATURE_HIGH:
            alerts.append({
                "patient_id": patient_id,
                "device_id": reading["device_id"],
                "alert_type": "temperature_high",
                "message": f"Temperatura elevada: {temperature}°C",
                "value": temperature,
                "severity": "medium"
            })
        
        if alerts:
            logger.info(f"Gerados {len(alerts)} alertas para paciente {patient_id}")
        
        return alerts
    
    @staticmethod
    def get_alert_messages(alerts: List[Dict]) -> List[str]:
        """Extrair mensagens dos alertas"""
        return [alert["message"] for alert in alerts]

# Instância global do serviço de alertas
alert_service = AlertService()