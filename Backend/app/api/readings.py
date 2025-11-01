from fastapi import APIRouter, HTTPException, status
from app.models.schemas import BiometricReadingCreate, ReadingResponse, PatientReadings
from app.services.database import db_service
from app.services.alert_service import alert_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/readings", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
async def create_reading(reading: BiometricReadingCreate):
    """
    Criar nova leitura biomédica
    
    - **device_id**: Identificador único do dispositivo ESP32
    - **heart_rate**: Frequência cardíaca em BPM (30-200)
    - **temperature**: Temperatura corporal em Celsius (30-45)
    """
    try:
        # Por simplicidade, usar device_id como patient_id
        patient_id = reading.device_id
        
        # Converter para dict
        reading_dict = reading.dict()
        
        # Processar alertas
        alerts = alert_service.process_reading_alerts(reading_dict, patient_id)
        alert_messages = alert_service.get_alert_messages(alerts)
        
        # Salvar leitura
        reading_id = db_service.save_reading(reading_dict, patient_id)
        
        # Salvar alertas
        for alert in alerts:
            db_service.save_alert(alert)
        
        # Atualizar status do dispositivo
        db_service.update_device_status(reading.device_id, patient_id)
        
        logger.info(f"Leitura criada: {reading_id}, Alertas: {len(alerts)}")
        
        return ReadingResponse(
            status="success",
            reading_id=reading_id,
            alerts_count=len(alerts),
            alerts=alert_messages
        )
        
    except Exception as e:
        logger.error(f"Erro ao criar leitura: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/readings/device/{device_id}", response_model=PatientReadings)
def get_device_readings(device_id: str, limit: int = 100):
    """
    Buscar leituras de um dispositivo específico
    
    - **device_id**: Identificador do dispositivo
    - **limit**: Número máximo de leituras (padrão: 100)
    """
    try:
        readings = db_service.get_device_readings(device_id, limit)
        
        if not readings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma leitura encontrada para este dispositivo"
            )
        
        # Usar device_id como patient_id para estatísticas
        patient_id = device_id
        statistics = db_service.get_reading_statistics(patient_id)
        
        return PatientReadings(
            patient_id=patient_id,
            device_id=device_id,
            readings=readings,
            total_count=len(readings),
            statistics=statistics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar leituras: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/readings/patient/{patient_id}/alerts")
def get_patient_alerts(patient_id: str, limit: int = 50):
    """
    Buscar alertas de um paciente
    
    - **patient_id**: Identificador do paciente
    - **limit**: Número máximo de alertas (padrão: 50)
    """
    try:
        alerts = db_service.get_patient_alerts(patient_id, limit)
        
        return {
            "patient_id": patient_id,
            "alerts": alerts,
            "total_count": len(alerts)
        }
        
    except Exception as e:
        logger.error(f"Erro ao buscar alertas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )