from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.models import DeviceType, WebAppExperienceResponse
from app.ml_model import classifier
from app.advanced_flow_classifier import AdvancedFlowClassifier

# Crear la aplicación FastAPI
app = FastAPI(
    title="Web App Experience Service",
    description="Servicio para procesar experiencia web y app con ML",
    version="0.1.0"
)

# Configurar CORS para permitir requests desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar los modelos al arrancar la aplicación
@app.on_event("startup")
async def startup_event():
    """Inicializa los modelos de ML al arrancar la aplicación"""
    try:
        classifier.load_model()
        print("✅ Modelo básico de clasificación inicializado correctamente")
    except Exception as e:
        print(f"⚠️ Error cargando modelo básico: {e}")
        print("🔄 Entrenando nuevo modelo básico...")
        classifier.train()
    
    # Inicializar modelo avanzado
    global advanced_classifier
    advanced_classifier = AdvancedFlowClassifier()
    try:
        if advanced_classifier.load_model():
            print("✅ Modelo avanzado de flujos inicializado correctamente")
        else:
            print("🔄 Entrenando modelo avanzado...")
            advanced_classifier.train()
    except Exception as e:
        print(f"⚠️ Error con modelo avanzado: {e}")
        print("🔄 Entrenando nuevo modelo avanzado...")
        advanced_classifier.train()


@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servicio esté funcionando"""
    return {"message": "Web App Experience Service está funcionando"}


@app.get("/web-and-app-experience")
async def get_web_app_experience(
    wifi: bool = Query(..., description="Estado de la conexión WiFi"),
    device: DeviceType = Query(..., description="Tipo de dispositivo (android/ios)"),
    latitude: float = Query(None, description="Latitud del usuario"),
    longitude: float = Query(None, description="Longitud del usuario"),
    network_speed: float = Query(None, description="Velocidad de red en Mbps")
) -> WebAppExperienceResponse:
    """
    Procesa la experiencia web y app con 8 features incluyendo geocercas
    usando un modelo de regresión logística para clasificar la calidad de conexión
    
    Args:
        wifi: boolean - Estado de la conexión WiFi
        device: string - Tipo de dispositivo (android/ios)
        latitude: float - Latitud del usuario (opcional)
        longitude: float - Longitud del usuario (opcional)
        network_speed: float - Velocidad de red en Mbps (opcional)
    
    Returns:
        WebAppExperienceResponse: Clasificación de la calidad de conexión
    """
    try:
        print(f"Procesando request: wifi={wifi}, device={device}, lat={latitude}, lon={longitude}, speed={network_speed}")
        
        # Usar el modelo de ML para clasificar la conexión
        prediction = classifier.predict(wifi, device.value, latitude, longitude, network_speed)
        
        # Crear la respuesta
        response = WebAppExperienceResponse(
            flow_type=prediction["flow_type"],
            connection_quality=prediction["connection_quality"],
            confidence_score=prediction["confidence_score"],
            prediction_reason=prediction["prediction_reason"],
            features_used=prediction["features_used"],
            location_info=prediction["location_info"]
        )
        
        print(f"Predicción: {prediction}")
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la solicitud: {str(e)}")


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "model_trained": classifier.is_trained}


@app.post("/retrain-model")
async def retrain_model():
    """Endpoint para re-entrenar el modelo con nuevos datos"""
    try:
        classifier.train()
        classifier.save_model()
        return {"message": "Modelo re-entrenado exitosamente", "accuracy": classifier.model.score(*classifier._create_training_data())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error re-entrenando el modelo: {str(e)}")


@app.get("/model-info")
async def get_model_info():
    """Endpoint para obtener información del modelo básico"""
    if classifier.is_trained:
        return {
            "model_type": "LogisticRegression",
            "is_trained": True,
            "features": [
                "wifi", "device_android", "device_ios",
                "latitude", "longitude", "distance_to_center",
                "is_urban_area", "network_speed"
            ],
            "total_features": 8,
            "classes": ["mala_conexion", "buena_conexion"],
            "geofencing_enabled": True
        }
    else:
        return {"is_trained": False, "message": "Modelo no entrenado"}


# ===== ENDPOINTS DEL MODELO AVANZADO =====

@app.get("/advanced-flow/predict")
async def predict_advanced_flow(
    wifi: bool = Query(..., description="Estado de la conexión WiFi"),
    device: DeviceType = Query(..., description="Tipo de dispositivo (android/ios)"),
    latitude: float = Query(..., description="Latitud del usuario"),
    longitude: float = Query(..., description="Longitud del usuario"),
    network_speed: float = Query(None, description="Velocidad de red en Mbps"),
    battery_level: float = Query(None, description="Nivel de batería (0-100)"),
    time_of_day: int = Query(None, description="Hora del día (0-23)")
):
    """
    Predice el flujo de experiencia usando el modelo avanzado con 5 tipos de flujo
    basado en 12 features incluyendo geocercas, plusvalía, batería y hora del día
    """
    try:
        print(f"Predicción avanzada: wifi={wifi}, device={device}, lat={latitude}, lon={longitude}")
        
        prediction = advanced_classifier.predict(
            wifi, device.value, latitude, longitude, 
            network_speed, battery_level, time_of_day
        )
        
        return prediction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción avanzada: {str(e)}")


@app.post("/advanced-flow/train")
async def train_advanced_model():
    """Entrena el modelo avanzado con nuevos datos"""
    try:
        result = advanced_classifier.train()
        return {
            "message": "Modelo avanzado entrenado exitosamente",
            "accuracy": result['accuracy'],
            "total_samples": result['total_samples'],
            "flow_distribution": result['flow_distribution']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error entrenando modelo avanzado: {str(e)}")


@app.get("/advanced-flow/info")
async def get_advanced_model_info():
    """Obtiene información del modelo avanzado"""
    try:
        return advanced_classifier.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo info del modelo avanzado: {str(e)}")


@app.get("/advanced-flow/compare")
async def compare_flows(
    wifi1: bool = Query(..., description="WiFi para ubicación 1"),
    device1: DeviceType = Query(..., description="Dispositivo para ubicación 1"),
    lat1: float = Query(..., description="Latitud 1"),
    lon1: float = Query(..., description="Longitud 1"),
    wifi2: bool = Query(..., description="WiFi para ubicación 2"),
    device2: DeviceType = Query(..., description="Dispositivo para ubicación 2"),
    lat2: float = Query(..., description="Latitud 2"),
    lon2: float = Query(..., description="Longitud 2")
):
    """Compara flujos entre dos ubicaciones diferentes"""
    try:
        prediction1 = advanced_classifier.predict(wifi1, device1.value, lat1, lon1)
        prediction2 = advanced_classifier.predict(wifi2, device2.value, lat2, lon2)
        
        return {
            "location_1": {
                "coordinates": (lat1, lon1),
                "prediction": prediction1
            },
            "location_2": {
                "coordinates": (lat2, lon2),
                "prediction": prediction2
            },
            "comparison": {
                "same_flow": prediction1['flow_type'] == prediction2['flow_type'],
                "flow_difference": f"{prediction1['flow_name']} vs {prediction2['flow_name']}"
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparando flujos: {str(e)}")
