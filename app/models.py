from enum import Enum
from pydantic import BaseModel


class DeviceType(str, Enum):
    """Tipos de dispositivos soportados"""
    ANDROID = "android"
    IOS = "ios"


class WebAppExperienceRequest(BaseModel):
    """Modelo para la solicitud de experiencia web y app"""
    wifi: bool
    device: DeviceType
    latitude: float = None
    longitude: float = None
    network_speed: float = None


class WebAppExperienceResponse(BaseModel):
    """Modelo para la respuesta de experiencia web y app"""
    flow_type: str
    connection_quality: str
    confidence_score: float
    prediction_reason: str
    features_used: int
    location_info: dict
