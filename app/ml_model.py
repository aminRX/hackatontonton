import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os


class ConnectionQualityClassifier:
    """Clasificador de calidad de conexión usando regresión logística"""
    
    def __init__(self):
        self.model = LogisticRegression(random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _create_training_data(self):
        """Crea datos de entrenamiento sintéticos con 8 features incluyendo geocercas"""
        # Generamos 2000 muestras de entrenamiento (más datos para más features)
        n_samples = 2000
        
        # Features: [wifi, device_android, device_ios, latitude, longitude, distance_to_center, is_urban_area, network_speed]
        
        X = []
        y = []
        
        for _ in range(n_samples):
            # Features básicas
            wifi = np.random.choice([0, 1], p=[0.3, 0.7])  # 70% con wifi
            device_android = np.random.choice([0, 1], p=[0.5, 0.5])
            device_ios = 1 - device_android if device_android == 1 else np.random.choice([0, 1], p=[0.5, 0.5])
            
            # Features de geocercas (ejemplo: Ciudad de México)
            latitude = np.random.uniform(19.0, 20.0)
            longitude = np.random.uniform(-99.5, -98.5)
            
            # Calcular distancia al centro
            center_lat, center_lon = 19.4326, -99.1332  # Centro CDMX
            distance_to_center = np.sqrt((latitude - center_lat)**2 + (longitude - center_lon)**2)
            
            # Features de ubicación y red
            is_urban_area = 1 if distance_to_center < 0.1 else 0
            network_speed = np.random.exponential(10) if wifi else np.random.exponential(2)
            
            # Regla de negocio mejorada con geocercas
            base_good_connection = wifi == 1 and (device_android == 1 or device_ios == 1)
            
            # Factores adicionales
            good_location = is_urban_area == 1
            good_speed = network_speed > 5
            
            # Calcular score de calidad
            quality_score = sum([
                base_good_connection * 3,  # Factor principal
                good_location * 1,         # Ubicación urbana
                good_speed * 1             # Buena velocidad
            ])
            
            # Clasificar como buena conexión si score >= 3
            is_good_connection = quality_score >= 3
            
            # Agregar ruido para robustez
            if np.random.random() < 0.05:  # 5% de ruido
                is_good_connection = not is_good_connection
            
            # Crear feature vector con 8 features
            features = [
                wifi, device_android, device_ios,
                latitude, longitude, distance_to_center,
                is_urban_area, network_speed
            ]
            
            X.append(features)
            y.append(1 if is_good_connection else 0)
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Entrena el modelo con datos sintéticos"""
        X, y = self._create_training_data()
        
        # Escalamos los datos
        X_scaled = self.scaler.fit_transform(X)
        
        # Entrenamos el modelo
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        print(f"Modelo entrenado con {len(X)} muestras")
        print(f"Precisión en entrenamiento: {self.model.score(X_scaled, y):.3f}")
    
    def predict(self, wifi: bool, device: str, latitude: float = None, longitude: float = None, 
                network_speed: float = None) -> dict:
        """Predice la calidad de conexión con 8 features incluyendo geocercas"""
        if not self.is_trained:
            self.train()
        
        # Convertir inputs a formato numérico
        wifi_num = 1 if wifi else 0
        device_android = 1 if device == "android" else 0
        device_ios = 1 if device == "ios" else 0
        
        # Valores por defecto para geocercas si no se proporcionan
        if latitude is None:
            latitude = 19.4326  # Centro CDMX por defecto
        if longitude is None:
            longitude = -99.1332
        if network_speed is None:
            network_speed = 10.0 if wifi else 2.0  # Velocidad típica
        
        # Calcular distancia al centro
        center_lat, center_lon = 19.4326, -99.1332
        distance_to_center = np.sqrt((latitude - center_lat)**2 + (longitude - center_lon)**2)
        
        # Determinar si es área urbana
        is_urban_area = 1 if distance_to_center < 0.1 else 0
        
        # Preparar features con 8 parámetros
        features = np.array([[
            wifi_num, device_android, device_ios,
            latitude, longitude, distance_to_center,
            is_urban_area, network_speed
        ]])
        
        features_scaled = self.scaler.transform(features)
        
        # Predicción
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        # Determinar el flujo y calidad
        if prediction == 1:
            flow_type = "flow-1"
            connection_quality = "buena"
            confidence_score = probability[1]
            
            # Crear razón detallada
            reasons = []
            if wifi:
                reasons.append("WiFi activo")
            if device_android or device_ios:
                reasons.append(f"dispositivo {device}")
            if is_urban_area:
                reasons.append("ubicación urbana")
            if network_speed > 5:
                reasons.append("buena velocidad de red")
            
            prediction_reason = f"Usuario con {' + '.join(reasons)}"
        else:
            flow_type = "flow-2"
            connection_quality = "mala"
            confidence_score = probability[0]
            
            # Crear razón detallada
            reasons = []
            if not wifi:
                reasons.append("sin WiFi")
            if not (device_android or device_ios):
                reasons.append("dispositivo no compatible")
            if not is_urban_area:
                reasons.append("ubicación no urbana")
            if network_speed <= 5:
                reasons.append("velocidad de red baja")
            
            prediction_reason = f"Usuario {' + '.join(reasons)}"
        
        return {
            "flow_type": flow_type,
            "connection_quality": connection_quality,
            "confidence_score": round(confidence_score, 3),
            "prediction_reason": prediction_reason,
            "features_used": 8,
            "location_info": {
                "latitude": round(latitude, 4),
                "longitude": round(longitude, 4),
                "distance_to_center": round(distance_to_center, 4),
                "is_urban_area": bool(is_urban_area)
            }
        }
    
    def save_model(self, filepath: str = "connection_classifier.joblib"):
        """Guarda el modelo entrenado"""
        if self.is_trained:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, filepath)
            print(f"Modelo guardado en {filepath}")
    
    def load_model(self, filepath: str = "connection_classifier.joblib"):
        """Carga un modelo pre-entrenado"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.is_trained = model_data['is_trained']
            print(f"Modelo cargado desde {filepath}")
        else:
            print("No se encontró modelo pre-entrenado, entrenando nuevo modelo...")
            self.train()


# Instancia global del clasificador
classifier = ConnectionQualityClassifier()
