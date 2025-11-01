from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class BiometricReadingCreate(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=50)
    heart_rate: int = Field(..., ge=30, le=200, description="Batimentos por minuto")
    temperature: float = Field(..., ge=30.0, le=45.0, description="Temperatura corporal em Celsius")

class BiometricReading(BiometricReadingCreate):
    id: Optional[str] = None
    timestamp: datetime
    patient_id: str
    alerts: List[str] = []

class Alert(BaseModel):
    id: Optional[str] = None
    patient_id: str
    device_id: str
    alert_type: str
    message: str
    value: float
    severity: str
    timestamp: datetime
    resolved: bool = False

class DeviceStatus(BaseModel):
    device_id: str
    patient_id: Optional[str] = None
    status: str
    last_reading: Optional[datetime] = None
    total_readings: int = 0

class ReadingResponse(BaseModel):
    status: str
    reading_id: str
    alerts_count: int
    alerts: List[str]

class PatientReadings(BaseModel):
    patient_id: str
    device_id: str
    readings: List[BiometricReading]
    total_count: int
    statistics: dict