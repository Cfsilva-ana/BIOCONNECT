from fastapi import APIRouter, HTTPException, status
from app.services.database import db_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/devices")
def get_devices():
    """
    Listar todos os dispositivos conectados
    
    Retorna informações sobre status, última leitura e total de leituras
    """
    try:
        devices = db_service.get_devices()
        
        return {
            "devices": devices,
            "total_count": len(devices)
        }
        
    except Exception as e:
        logger.error(f"Erro ao buscar dispositivos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/devices/{device_id}/status")
def get_device_status(device_id: str):
    """
    Verificar status de um dispositivo específico
    
    - **device_id**: Identificador do dispositivo
    """
    try:
        devices = db_service.get_devices()
        device = next((d for d in devices if d["device_id"] == device_id), None)
        
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo não encontrado"
            )
        
        return device
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar status do dispositivo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )