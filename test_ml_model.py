#!/usr/bin/env python3
"""
Script de prueba para el modelo de clasificación con geocercas
"""

from app.ml_model import classifier
from app.models import DeviceType

def test_model_predictions():
    """Prueba el modelo con diferentes combinaciones de inputs incluyendo geocercas"""
    
    print("🤖 Probando modelo de clasificación con 8 features (geocercas)")
    print("=" * 70)
    
    # Casos de prueba con geocercas
    test_cases = [
        {
            'name': 'Caso 1: WiFi ON + Android + Urbano + Buena velocidad',
            'wifi': True,
            'device': DeviceType.ANDROID,
            'latitude': 19.4326,
            'longitude': -99.1332,
            'network_speed': 15.0
        },
        {
            'name': 'Caso 2: WiFi OFF + iOS + Rural + Baja velocidad',
            'wifi': False,
            'device': DeviceType.IOS,
            'latitude': 19.8,
            'longitude': -99.0,
            'network_speed': 1.5
        },
        {
            'name': 'Caso 3: WiFi ON + iOS + Suburbano + Velocidad media',
            'wifi': True,
            'device': DeviceType.IOS,
            'latitude': 19.3,
            'longitude': -99.2,
            'network_speed': 8.0
        },
        {
            'name': 'Caso 4: WiFi ON + Android + Centro urbano + Alta velocidad',
            'wifi': True,
            'device': DeviceType.ANDROID,
            'latitude': 19.4326,
            'longitude': -99.1332,
            'network_speed': 25.0
        }
    ]
    
    for case in test_cases:
        print(f"\n📱 {case['name']}")
        print(f"   Input: wifi={case['wifi']}, device={case['device'].value}")
        print(f"   Location: ({case['latitude']}, {case['longitude']})")
        print(f"   Speed: {case['network_speed']} Mbps")
        
        prediction = classifier.predict(
            case['wifi'], 
            case['device'].value,
            case['latitude'],
            case['longitude'],
            case['network_speed']
        )
        
        print(f"   Resultado: {prediction['flow_type']}")
        print(f"   Calidad: {prediction['connection_quality']}")
        print(f"   Confianza: {prediction['confidence_score']}")
        print(f"   Razón: {prediction['prediction_reason']}")
        print(f"   Features usadas: {prediction['features_used']}")
        print(f"   Info ubicación: {prediction['location_info']}")
    
    print("\n" + "=" * 70)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    test_model_predictions()
