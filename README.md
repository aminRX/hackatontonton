# 🚀 Sistema de Clasificación de Flujos de Experiencia Web/App

## 📋 Descripción General

Este proyecto implementa un sistema de Machine Learning para clasificar la calidad de experiencia de usuarios web y móviles basado en múltiples factores incluyendo geocercas, plusvalía, condiciones de red y estado del dispositivo.

## 🎯 Características Principales

### 🤖 **Dos Modelos de ML:**
1. **Modelo Básico**: Regresión Logística (2 flujos)
2. **Modelo Avanzado**: Random Forest (5 flujos)

### 🗺️ **Geocercas de CDMX:**
- **9 zonas reales** con coordenadas precisas
- **4 niveles de plusvalía**: alta, media, baja, emergente
- **Factores de calidad** específicos por zona

### 📊 **Features Avanzadas:**
- WiFi y tipo de dispositivo
- Coordenadas geográficas
- Velocidad de red
- Nivel de batería
- Hora del día
- Factor de calidad de zona
- Cobertura WiFi

## 🏗️ Arquitectura del Proyecto

```
hackaton/
├── app/
│   ├── main.py                    # FastAPI endpoints
│   ├── models.py                  # Pydantic models
│   ├── ml_model.py               # Modelo básico (LogisticRegression)
│   └── advanced_flow_classifier.py # Modelo avanzado (RandomForest)
├── test_ml_model.py              # Tests modelo básico
├── test_advanced_training.py     # Tests modelo avanzado
├── visualize_model.py            # Visualizaciones
├── pyproject.toml                # Dependencias
└── README.md                     # Este archivo
```

## 🗺️ Geocercas Implementadas

### 🏙️ **Alta Plusvalía:**
- **Polanco**: (19.4333, -99.2000) - Factor 1.3, WiFi 95%
- **Condesa**: (19.4100, -99.1800) - Factor 1.2, WiFi 90%
- **Roma**: (19.4200, -99.1600) - Factor 1.1, WiFi 85%

### 🏘️ **Media Plusvalía:**
- **Centro Histórico**: (19.4326, -99.1332) - Factor 0.9, WiFi 70%
- **Coyoacán**: (19.3500, -99.1600) - Factor 0.8, WiFi 60%

### 🏠 **Baja Plusvalía:**
- **Iztapalapa**: (19.3550, -99.0900) - Factor 0.7, WiFi 45%
- **Gustavo Madero**: (19.4800, -99.1100) - Factor 0.6, WiFi 40%

### 🌾 **Emergente:**
- **Tláhuac**: (19.2800, -99.0100) - Factor 0.5, WiFi 30%
- **Milpa Alta**: (19.1900, -99.0200) - Factor 0.4, WiFi 25%

## 🤖 Modelos de Machine Learning

### 📊 **Modelo Básico (LogisticRegression)**
- **Features**: 8
- **Flujos**: 2 (flow-1: buena, flow-2: mala)
- **Algoritmo**: Regresión Logística
- **Uso**: Clasificación binaria de calidad de conexión

**Features:**
1. `wifi` - Estado de conexión WiFi
2. `device_android` - Dispositivo Android
3. `device_ios` - Dispositivo iOS
4. `latitude` - Latitud del usuario
5. `longitude` - Longitud del usuario
6. `distance_to_center` - Distancia al centro de CDMX
7. `is_urban_area` - Si está en zona urbana
8. `network_speed` - Velocidad de red en Mbps

### 🚀 **Modelo Avanzado (RandomForest)**
- **Features**: 12
- **Flujos**: 5 (Premium, Estándar, Básica, Ligera, Offline)
- **Algoritmo**: Random Forest
- **Uso**: Clasificación multiclase de experiencia de usuario

**Features:**
1. `wifi` - Estado de conexión WiFi
2. `device_android` - Dispositivo Android
3. `device_ios` - Dispositivo iOS
4. `latitude` - Latitud del usuario
5. `longitude` - Longitud del usuario
6. `distance_to_center` - Distancia al centro de la zona
7. `quality_factor` - Factor de calidad de la zona
8. `wifi_coverage` - Cobertura WiFi de la zona
9. `network_speed` - Velocidad de red en Mbps
10. `battery_level` - Nivel de batería (0-100)
11. `time_of_day` - Hora del día (0-23)
12. `is_high_plusvalia` - Si es zona de alta plusvalía

## 🎯 Tipos de Flujo (Modelo Avanzado)

### 🏆 **Flow Premium**
- **Condiciones**: WiFi + Alta plusvalía + Velocidad >15Mbps + Batería >30% + Cobertura WiFi >80%
- **Experiencia**: Máxima calidad, todas las funciones disponibles

### ⭐ **Flow Estándar**
- **Condiciones**: WiFi + Velocidad >8Mbps + Batería >20%
- **Experiencia**: Calidad alta, mayoría de funciones disponibles

### 📱 **Flow Básica**
- **Condiciones**: WiFi + Velocidad moderada
- **Experiencia**: Funcionalidad básica, optimizada para conexiones lentas

### 🔋 **Flow Ligera**
- **Condiciones**: WiFi + Velocidad <5Mbps
- **Experiencia**: Versión minimalista, carga rápida

### 📴 **Flow Offline**
- **Condiciones**: Sin WiFi o velocidad <2Mbps
- **Experiencia**: Modo offline, contenido precargado

## 🚀 Instalación y Configuración

### 📋 **Prerrequisitos:**
- Python 3.8+
- Poetry (gestor de dependencias)

### 🔧 **Instalación:**

```bash
# Clonar el repositorio
git clone <repository-url>
cd hackaton

# Instalar dependencias
poetry install

# Activar el entorno virtual
poetry shell
```

### 🏃‍♂️ **Ejecutar el Servicio:**

```bash
# Iniciar el servidor
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servicio estará disponible en: `http://localhost:8000`

## 📚 API Endpoints

### 🔍 **Endpoints del Modelo Básico:**

#### `GET /web-and-app-experience`
Predice la calidad de conexión usando el modelo básico.

**Parámetros:**
- `wifi` (bool, requerido): Estado de WiFi
- `device` (string, requerido): "android" o "ios"
- `latitude` (float, opcional): Latitud del usuario
- `longitude` (float, opcional): Longitud del usuario
- `network_speed` (float, opcional): Velocidad de red en Mbps

**Ejemplo:**
```bash
curl "http://localhost:8000/web-and-app-experience?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0"
```

**Respuesta:**
```json
{
  "flow_type": "flow-1",
  "connection_quality": "buena",
  "confidence_score": 0.943,
  "prediction_reason": "Usuario con WiFi activo + dispositivo ios + ubicación urbana + buena velocidad de red",
  "features_used": 8,
  "location_info": {
    "latitude": 19.4333,
    "longitude": -99.2,
    "distance_to_center": 0.0668,
    "is_urban_area": true
  }
}
```

#### `GET /model-info`
Obtiene información del modelo básico.

#### `POST /retrain-model`
Re-entrena el modelo básico.

### 🚀 **Endpoints del Modelo Avanzado:**

#### `GET /advanced-flow/predict`
Predice el flujo de experiencia usando el modelo avanzado.

**Parámetros:**
- `wifi` (bool, requerido): Estado de WiFi
- `device` (string, requerido): "android" o "ios"
- `latitude` (float, requerido): Latitud del usuario
- `longitude` (float, requerido): Longitud del usuario
- `network_speed` (float, opcional): Velocidad de red en Mbps
- `battery_level` (float, opcional): Nivel de batería (0-100)
- `time_of_day` (int, opcional): Hora del día (0-23)

**Ejemplo:**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0&battery_level=85.0&time_of_day=14"
```

**Respuesta:**
```json
{
  "flow_type": "flow-premium",
  "flow_name": "Experiencia Premium",
  "confidence_score": 0.96,
  "zone_info": {
    "zone_name": "polanco",
    "plusvalia": "alta",
    "quality_factor": 1.3,
    "wifi_coverage": 0.95,
    "distance_to_center": 0.0
  },
  "network_conditions": {
    "wifi_active": true,
    "device_type": "ios",
    "network_speed": 25.0,
    "battery_level": 85.0,
    "time_of_day": 14
  },
  "features_used": 12,
  "model_type": "AdvancedFlowClassifier"
}
```

#### `GET /advanced-flow/info`
Obtiene información del modelo avanzado.

#### `POST /advanced-flow/train`
Re-entrena el modelo avanzado.

#### `GET /advanced-flow/compare`
Compara flujos entre dos ubicaciones diferentes.

**Ejemplo:**
```bash
curl "http://localhost:8000/advanced-flow/compare?wifi1=true&device1=ios&lat1=19.4333&lon1=-99.2000&wifi2=true&device2=android&lat2=19.3550&lon2=-99.0900"
```

### 🏥 **Endpoints de Sistema:**

#### `GET /health`
Verifica el estado del servicio.

#### `GET /`
Endpoint raíz con información básica.

## 🧪 Testing

### 📊 **Test del Modelo Básico:**
```bash
poetry run python test_ml_model.py
```

### 🚀 **Test del Modelo Avanzado:**
```bash
poetry run python test_advanced_training.py
```

### 📈 **Visualizaciones:**
```bash
poetry run python visualize_model.py
```

## 📊 Ejemplos de Uso

### 🏙️ **Ejemplo 1: Usuario en Polanco (Alta Plusvalía)**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=ios&latitude=19.4333&longitude=-99.2000&network_speed=25.0&battery_level=90.0&time_of_day=14"
```
**Resultado esperado:** `flow-premium` (Experiencia Premium)

### 🏠 **Ejemplo 2: Usuario en Iztapalapa (Baja Plusvalía)**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=true&device=android&latitude=19.3550&longitude=-99.0900&network_speed=8.0&battery_level=30.0&time_of_day=8"
```
**Resultado esperado:** `flow-basic` (Experiencia Básica)

### 🌾 **Ejemplo 3: Usuario en Milpa Alta (Emergente)**
```bash
curl "http://localhost:8000/advanced-flow/predict?wifi=false&device=android&latitude=19.1900&longitude=-99.0200&network_speed=1.0&battery_level=5.0&time_of_day=22"
```
**Resultado esperado:** `flow-offline` (Experiencia Offline)

## 🔧 Configuración Avanzada

### 📝 **Variables de Entorno:**
- `PORT`: Puerto del servidor (default: 8000)
- `HOST`: Host del servidor (default: 0.0.0.0)
- `DEBUG`: Modo debug (default: False)

### 🎛️ **Parámetros del Modelo:**
Los modelos se pueden configurar modificando los archivos:
- `app/ml_model.py` - Modelo básico
- `app/advanced_flow_classifier.py` - Modelo avanzado

### 🗺️ **Agregar Nuevas Geocercas:**
Para agregar nuevas zonas, edita el diccionario `geo_zones` en `app/advanced_flow_classifier.py`:

```python
'nombre_zona': {
    'center': (latitud, longitud),
    'radius': radio_en_grados,
    'plusvalia': 'alta|media|baja|emergente',
    'quality_factor': factor_0_a_2,
    'network_speed_range': (min_mbps, max_mbps),
    'wifi_coverage': porcentaje_0_a_1
}
```

## 📈 Métricas y Rendimiento

### 🎯 **Modelo Básico:**
- **Precisión típica**: 85-95%
- **Features**: 8
- **Tiempo de entrenamiento**: <1 minuto
- **Tiempo de predicción**: <10ms

### 🚀 **Modelo Avanzado:**
- **Precisión típica**: 95-99%
- **Features**: 12
- **Tiempo de entrenamiento**: 2-5 minutos
- **Tiempo de predicción**: <50ms
- **Muestras de entrenamiento**: 2000

## 🔍 Monitoreo y Logs

### 📊 **Logs del Servicio:**
- Inicialización de modelos
- Predicciones realizadas
- Errores y excepciones
- Métricas de rendimiento

### 📈 **Métricas Disponibles:**
- Precisión del modelo
- Distribución de flujos
- Tiempo de respuesta
- Uso de memoria

## 🛠️ Troubleshooting

### ❌ **Error: "Modelo no entrenado"**
```bash
# Re-entrenar el modelo
curl -X POST "http://localhost:8000/advanced-flow/train"
```

### ❌ **Error: "Valores infinitos"**
- Verificar coordenadas geográficas
- Revisar parámetros de entrada
- Re-entrenar el modelo

### ❌ **Error: "Puerto ocupado"**
```bash
# Cambiar puerto
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo
- Revisar la documentación de la API en `/docs` (cuando el servidor esté corriendo)

---

## 🎉 ¡Disfruta usando el Sistema de Clasificación de Flujos!

Este sistema te permite tomar decisiones inteligentes sobre la experiencia de usuario basadas en ubicación geográfica, condiciones de red y estado del dispositivo. ¡Experimenta con diferentes escenarios y optimiza la experiencia de tus usuarios! 🚀
