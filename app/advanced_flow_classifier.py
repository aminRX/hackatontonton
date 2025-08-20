import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class AdvancedFlowClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.model_path = "advanced_flow_model.joblib"
        
        # Definir geocercas reales de CDMX con plusvalía
        self.geo_zones = {
            'polanco': {
                'center': (19.4333, -99.2000),
                'radius': 0.02,
                'plusvalia': 'alta',
                'quality_factor': 1.3,
                'network_speed_range': (20, 60),
                'wifi_coverage': 0.95
            },
            'condesa': {
                'center': (19.4100, -99.1800),
                'radius': 0.015,
                'plusvalia': 'alta',
                'quality_factor': 1.2,
                'network_speed_range': (15, 45),
                'wifi_coverage': 0.9
            },
            'roma': {
                'center': (19.4200, -99.1600),
                'radius': 0.02,
                'plusvalia': 'alta',
                'quality_factor': 1.1,
                'network_speed_range': (12, 35),
                'wifi_coverage': 0.85
            },
            'centro_historico': {
                'center': (19.4326, -99.1332),
                'radius': 0.025,
                'plusvalia': 'media',
                'quality_factor': 0.9,
                'network_speed_range': (8, 25),
                'wifi_coverage': 0.7
            },
            'coyoacan': {
                'center': (19.3500, -99.1600),
                'radius': 0.03,
                'plusvalia': 'media',
                'quality_factor': 0.8,
                'network_speed_range': (6, 20),
                'wifi_coverage': 0.6
            },
            'iztapalapa': {
                'center': (19.3550, -99.0900),
                'radius': 0.03,
                'plusvalia': 'baja',
                'quality_factor': 0.7,
                'network_speed_range': (3, 12),
                'wifi_coverage': 0.45
            },
            'gustavo_madero': {
                'center': (19.4800, -99.1100),
                'radius': 0.035,
                'plusvalia': 'baja',
                'quality_factor': 0.6,
                'network_speed_range': (2, 10),
                'wifi_coverage': 0.4
            },
            'tlahuac': {
                'center': (19.2800, -99.0100),
                'radius': 0.04,
                'plusvalia': 'emergente',
                'quality_factor': 0.5,
                'network_speed_range': (1, 8),
                'wifi_coverage': 0.3
            },
            'milpa_alta': {
                'center': (19.1900, -99.0200),
                'radius': 0.05,
                'plusvalia': 'emergente',
                'quality_factor': 0.4,
                'network_speed_range': (1, 5),
                'wifi_coverage': 0.25
            }
        }
    
    def _get_zone_info(self, latitude: float, longitude: float):
        """Obtiene información de la zona geográfica más cercana"""
        closest_zone = None
        min_distance = float('inf')
        
        for zone_name, zone_data in self.geo_zones.items():
            center_lat, center_lon = zone_data['center']
            distance = np.sqrt((latitude - center_lat)**2 + (longitude - center_lon)**2)
            
            if distance <= zone_data['radius'] and distance < min_distance:
                closest_zone = zone_name
                min_distance = distance
        
        if closest_zone:
            zone_data = self.geo_zones[closest_zone]
            return {
                'zone_name': closest_zone,
                'plusvalia': zone_data['plusvalia'],
                'quality_factor': zone_data['quality_factor'],
                'wifi_coverage': zone_data['wifi_coverage'],
                'distance_to_center': min_distance
            }
        else:
            return {
                'zone_name': 'unknown',
                'plusvalia': 'baja',
                'quality_factor': 0.5,
                'wifi_coverage': 0.3,
                'distance_to_center': min_distance
            }
    
    def _determine_flow_type(self, wifi: bool, zone_info: dict, network_speed: float, 
                           battery_level: float, time_of_day: int) -> str:
        """Determina el tipo de flujo basado en las condiciones"""
        
        # Sin WiFi = Offline
        if not wifi or network_speed < 2:
            return 'flow-offline'
        
        # Velocidad muy baja = Light
        if network_speed < 5:
            return 'flow-light'
        
        # Condiciones premium
        if (zone_info['plusvalia'] == 'alta' and 
            network_speed > 15 and 
            battery_level > 30 and
            zone_info['wifi_coverage'] > 0.8):
            return 'flow-premium'
        
        # Condiciones estándar
        if network_speed > 8 and battery_level > 20:
            return 'flow-standard'
        
        # Condiciones básicas
        return 'flow-basic'
    
    def _create_advanced_training_data(self, n_samples=2000):
        """Genera datos de entrenamiento sintéticos para el modelo avanzado"""
        X = []
        y = []
        
        print(f"🔄 Generando {n_samples} muestras de entrenamiento...")
        
        for i in range(n_samples):
            # Features básicas
            wifi = np.random.choice([0, 1], p=[0.2, 0.8])  # 80% con WiFi
            device_android = np.random.choice([0, 1], p=[0.5, 0.5])
            device_ios = 1 - device_android
            
            # Seleccionar zona aleatoria
            zone_name = np.random.choice(list(self.geo_zones.keys()))
            zone_data = self.geo_zones[zone_name]
            
            # Generar coordenadas dentro de la zona
            center_lat, center_lon = zone_data['center']
            radius = zone_data['radius']
            
            # Usar distribución uniforme en lugar de normal para evitar valores extremos
            latitude = np.random.uniform(center_lat - radius/2, center_lat + radius/2)
            longitude = np.random.uniform(center_lon - radius/2, center_lon + radius/2)
            
            # Asegurar que las coordenadas estén dentro de límites razonables
            latitude = np.clip(latitude, 19.0, 20.0)
            longitude = np.clip(longitude, -99.5, -98.5)
            
            # Obtener información de la zona
            zone_info = self._get_zone_info(latitude, longitude)
            
            # Velocidad de red basada en la zona y WiFi
            min_speed, max_speed = zone_data['network_speed_range']
            if wifi:
                network_speed = np.random.uniform(min_speed * 0.7, max_speed)
            else:
                network_speed = np.random.uniform(0.5, 3)
            
            # Factores adicionales
            battery_level = np.random.uniform(5, 100)
            time_of_day = np.random.randint(0, 24)
            
            # Determinar flujo basado en condiciones
            flow_type = self._determine_flow_type(
                wifi, zone_info, network_speed, battery_level, time_of_day
            )
            
            # Crear feature vector (12 features)
            features = [
                wifi,
                device_android,
                device_ios,
                latitude,
                longitude,
                zone_info['distance_to_center'],
                zone_info['quality_factor'],
                zone_info['wifi_coverage'],
                network_speed,
                battery_level / 100.0,
                time_of_day / 24.0,
                1 if zone_info['plusvalia'] == 'alta' else 0
            ]
            
            X.append(features)
            y.append(flow_type)
            
            if (i + 1) % 500 == 0:
                print(f"   Generadas {i + 1} muestras...")
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Entrena el modelo avanzado"""
        print('🚀 Iniciando entrenamiento del modelo avanzado...')
        
        # Generar datos de entrenamiento
        X, y = self._create_advanced_training_data()
        
        # Verificar que no hay valores infinitos en los datos originales
        if np.any(np.isinf(X)) or np.any(np.isnan(X)):
            print("⚠️ Detectados valores infinitos en datos originales, limpiando...")
            X = np.nan_to_num(X, nan=0.0, posinf=1.0, neginf=-1.0)
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        print(f'📊 Datos de entrenamiento: {len(X_train)} muestras')
        print(f'📊 Datos de prueba: {len(X_test)} muestras')
        
        # Escalar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Verificar que no hay valores infinitos después del escalado
        if np.any(np.isinf(X_train_scaled)) or np.any(np.isinf(X_test_scaled)):
            print("⚠️ Detectados valores infinitos después del escalado, reemplazando...")
            X_train_scaled = np.nan_to_num(X_train_scaled, nan=0.0, posinf=1.0, neginf=-1.0)
            X_test_scaled = np.nan_to_num(X_test_scaled, nan=0.0, posinf=1.0, neginf=-1.0)
        
        # Codificar labels
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        y_test_encoded = self.label_encoder.transform(y_test)
        
        # Entrenar modelo
        print('🤖 Entrenando Random Forest...')
        self.model.fit(X_train_scaled, y_train_encoded)
        self.is_trained = True
        
        # Evaluar modelo
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test_encoded, y_pred)
        
        print(f'✅ Modelo entrenado exitosamente!')
        print(f'📈 Precisión en test: {accuracy:.3f}')
        
        # Mostrar distribución de flujos
        unique, counts = np.unique(y_train, return_counts=True)
        print(f'📊 Distribución de flujos:')
        for flow, count in zip(unique, counts):
            print(f'   {flow}: {count} muestras')
        
        # Guardar modelo
        self.save_model()
        
        return {
            'accuracy': accuracy,
            'total_samples': len(X),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'flow_distribution': dict(zip(unique, counts))
        }
    
    def predict(self, wifi: bool, device: str, latitude: float, longitude: float, 
               network_speed: float = None, battery_level: float = None, 
               time_of_day: int = None):
        """Realiza predicción con el modelo avanzado"""
        
        if not self.is_trained:
            print('⚠️ Modelo no entrenado. Entrenando...')
            self.train()
        
        # Convertir inputs
        wifi_num = 1 if wifi else 0
        device_android = 1 if device == 'android' else 0
        device_ios = 1 if device == 'ios' else 0
        
        # Obtener información de zona
        zone_info = self._get_zone_info(latitude, longitude)
        
        # Valores por defecto
        if network_speed is None:
            if wifi:
                network_speed = np.random.uniform(5, 25)
            else:
                network_speed = np.random.uniform(1, 3)
        
        if battery_level is None:
            battery_level = np.random.uniform(20, 100)
        
        if time_of_day is None:
            time_of_day = np.random.randint(0, 24)
        
        # Crear feature vector
        features = np.array([[
            wifi_num,
            device_android,
            device_ios,
            latitude,
            longitude,
            zone_info['distance_to_center'],
            zone_info['quality_factor'],
            zone_info['wifi_coverage'],
            network_speed,
            battery_level / 100.0,
            time_of_day / 24.0,
            1 if zone_info['plusvalia'] == 'alta' else 0
        ]])
        
        # Escalar features
        features_scaled = self.scaler.transform(features)
        
        # Verificar que no hay valores infinitos
        if np.any(np.isinf(features_scaled)):
            features_scaled = np.nan_to_num(features_scaled, nan=0.0, posinf=1.0, neginf=-1.0)
        
        # Predicción
        prediction_encoded = self.model.predict(features_scaled)[0]
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Probabilidades
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = max(probabilities)
        
        # Nombres de flujos
        flow_names = {
            'flow-premium': 'Experiencia Premium',
            'flow-standard': 'Experiencia Estándar',
            'flow-basic': 'Experiencia Básica',
            'flow-light': 'Experiencia Ligera',
            'flow-offline': 'Experiencia Offline'
        }
        
        return {
            'flow_type': prediction,
            'flow_name': flow_names.get(prediction, 'Experiencia Desconocida'),
            'confidence_score': round(confidence, 3),
            'zone_info': zone_info,
            'network_conditions': {
                'wifi_active': wifi,
                'device_type': device,
                'network_speed': round(network_speed, 1),
                'battery_level': round(battery_level, 1),
                'time_of_day': time_of_day
            },
            'features_used': 12,
            'model_type': 'AdvancedFlowClassifier'
        }
    
    def save_model(self):
        """Guarda el modelo entrenado"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, self.model_path)
        print(f'💾 Modelo guardado en {self.model_path}')
    
    def load_model(self):
        """Carga el modelo entrenado"""
        if os.path.exists(self.model_path):
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.label_encoder = model_data['label_encoder']
            self.is_trained = model_data['is_trained']
            print(f'📂 Modelo cargado desde {self.model_path}')
            return True
        else:
            print(f'⚠️ No se encontró modelo guardado en {self.model_path}')
            return False
    
    def get_model_info(self):
        """Obtiene información del modelo"""
        return {
            'model_type': 'RandomForestClassifier',
            'is_trained': self.is_trained,
            'features': [
                'wifi', 'device_android', 'device_ios', 'latitude', 'longitude',
                'distance_to_center', 'quality_factor', 'wifi_coverage',
                'network_speed', 'battery_level', 'time_of_day', 'is_high_plusvalia'
            ],
            'total_features': 12,
            'classes': list(self.label_encoder.classes_) if self.is_trained else [],
            'geo_zones': len(self.geo_zones),
            'plusvalia_levels': ['alta', 'media', 'baja', 'emergente']
        }
