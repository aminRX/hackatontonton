#!/usr/bin/env python3
"""
Script para probar el modelo avanzado de clasificación de flujos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.advanced_flow_classifier import AdvancedFlowClassifier
from app.ml_model import classifier

def test_advanced_model():
    """Prueba el modelo avanzado con diferentes escenarios"""
    
    print("🚀 PROBANDO MODELO AVANZADO DE FLUJOS")
    print("=" * 60)
    
    # Crear instancia del modelo avanzado
    advanced = AdvancedFlowClassifier()
    
    # Entrenar el modelo
    print("\n📚 Entrenando modelo avanzado...")
    result = advanced.train()
    
    print(f"\n✅ Entrenamiento completado!")
    print(f"📊 Precisión: {result['accuracy']:.3f}")
    print(f"📊 Muestras totales: {result['total_samples']}")
    print(f"📊 Distribución de flujos:")
    for flow, count in result['flow_distribution'].items():
        print(f"   {flow}: {count} muestras")
    
    # Escenarios de prueba
    test_scenarios = [
        {
            'name': 'Polanco - Condiciones Premium',
            'wifi': True,
            'device': 'ios',
            'latitude': 19.4333,
            'longitude': -99.2000,
            'network_speed': 25.0,
            'battery_level': 85.0,
            'time_of_day': 14
        },
        {
            'name': 'Condesa - Condiciones Estándar',
            'wifi': True,
            'device': 'android',
            'latitude': 19.4100,
            'longitude': -99.1800,
            'network_speed': 15.0,
            'battery_level': 60.0,
            'time_of_day': 10
        },
        {
            'name': 'Centro Histórico - Condiciones Básicas',
            'wifi': True,
            'device': 'android',
            'latitude': 19.4326,
            'longitude': -99.1332,
            'network_speed': 8.0,
            'battery_level': 30.0,
            'time_of_day': 20
        },
        {
            'name': 'Iztapalapa - Condiciones Light',
            'wifi': True,
            'device': 'ios',
            'latitude': 19.3550,
            'longitude': -99.0900,
            'network_speed': 3.0,
            'battery_level': 15.0,
            'time_of_day': 8
        },
        {
            'name': 'Milpa Alta - Condiciones Offline',
            'wifi': False,
            'device': 'android',
            'latitude': 19.1900,
            'longitude': -99.0200,
            'network_speed': 1.0,
            'battery_level': 5.0,
            'time_of_day': 22
        }
    ]
    
    print(f"\n📱 PROBANDO PREDICCIONES AVANZADAS:")
    print("-" * 60)
    
    for scenario in test_scenarios:
        print(f"\n📍 {scenario['name']}")
        print(f"   Coordenadas: ({scenario['latitude']}, {scenario['longitude']})")
        print(f"   WiFi: {scenario['wifi']}, Dispositivo: {scenario['device']}")
        print(f"   Velocidad: {scenario['network_speed']} Mbps")
        print(f"   Batería: {scenario['battery_level']}%, Hora: {scenario['time_of_day']}:00")
        
        # Predicción avanzada
        result = advanced.predict(
            scenario['wifi'],
            scenario['device'],
            scenario['latitude'],
            scenario['longitude'],
            scenario['network_speed'],
            scenario['battery_level'],
            scenario['time_of_day']
        )
        
        print(f"   🎯 Flujo: {result['flow_name']} ({result['flow_type']})")
        print(f"   🎯 Zona: {result['zone_info']['zone_name']}")
        print(f"   🎯 Plusvalía: {result['zone_info']['plusvalia']}")
        print(f"   🎯 Confianza: {result['confidence_score']}")
    
    return advanced

def compare_models():
    """Compara el modelo básico con el avanzado"""
    
    print(f"\n🔄 COMPARANDO MODELOS")
    print("=" * 60)
    
    # Asegurar que el modelo básico esté entrenado
    if not classifier.is_trained:
        print("Entrenando modelo básico...")
        classifier.train()
    
    # Crear modelo avanzado
    advanced = AdvancedFlowClassifier()
    if not advanced.is_trained:
        print("Entrenando modelo avanzado...")
        advanced.train()
    
    # Escenario de comparación
    test_case = {
        'wifi': True,
        'device': 'ios',
        'latitude': 19.4333,
        'longitude': -99.2000,
        'network_speed': 20.0
    }
    
    print(f"\n📊 Comparación de modelos:")
    print(f"   Coordenadas: ({test_case['latitude']}, {test_case['longitude']})")
    print(f"   WiFi: {test_case['wifi']}, Dispositivo: {test_case['device']}")
    print(f"   Velocidad: {test_case['network_speed']} Mbps")
    
    # Predicción modelo básico
    basic_result = classifier.predict(
        test_case['wifi'],
        test_case['device'],
        test_case['latitude'],
        test_case['longitude'],
        test_case['network_speed']
    )
    
    # Predicción modelo avanzado
    advanced_result = advanced.predict(
        test_case['wifi'],
        test_case['device'],
        test_case['latitude'],
        test_case['longitude'],
        test_case['network_speed']
    )
    
    print(f"\n🔹 MODELO BÁSICO:")
    print(f"   Flujo: {basic_result['flow_type']}")
    print(f"   Calidad: {basic_result['connection_quality']}")
    print(f"   Confianza: {basic_result['confidence_score']}")
    print(f"   Features: {basic_result['features_used']}")
    
    print(f"\n🔹 MODELO AVANZADO:")
    print(f"   Flujo: {advanced_result['flow_name']} ({advanced_result['flow_type']})")
    print(f"   Zona: {advanced_result['zone_info']['zone_name']}")
    print(f"   Plusvalía: {advanced_result['zone_info']['plusvalia']}")
    print(f"   Confianza: {advanced_result['confidence_score']}")
    print(f"   Features: {advanced_result['features_used']}")
    
    print(f"\n📈 DIFERENCIAS:")
    print(f"   - Modelo básico: 2 flujos (flow-1/flow-2)")
    print(f"   - Modelo avanzado: 5 flujos (premium/standard/basic/light/offline)")
    print(f"   - Modelo básico: 8 features")
    print(f"   - Modelo avanzado: 12 features (incluye batería, hora, plusvalía)")
    print(f"   - Modelo avanzado: Geocercas reales de CDMX")

def test_plusvalia_comparison():
    """Prueba diferentes niveles de plusvalía"""
    
    print(f"\n🏘️ COMPARACIÓN POR PLUSVALÍA")
    print("=" * 60)
    
    advanced = AdvancedFlowClassifier()
    if not advanced.is_trained:
        advanced.train()
    
    plusvalia_zones = [
        ('Polanco', 19.4333, -99.2000, 'alta'),
        ('Centro Histórico', 19.4326, -99.1332, 'media'),
        ('Iztapalapa', 19.3550, -99.0900, 'baja'),
        ('Milpa Alta', 19.1900, -99.0200, 'emergente')
    ]
    
    for zone_name, lat, lon, plusvalia in plusvalia_zones:
        print(f"\n📍 {zone_name} (Plusvalía: {plusvalia})")
        
        result = advanced.predict(
            wifi=True,
            device='ios',
            latitude=lat,
            longitude=lon,
            network_speed=15.0,
            battery_level=70.0,
            time_of_day=12
        )
        
        print(f"   Flujo: {result['flow_name']}")
        print(f"   Zona detectada: {result['zone_info']['zone_name']}")
        print(f"   Factor de calidad: {result['zone_info']['quality_factor']}")
        print(f"   Cobertura WiFi: {result['zone_info']['wifi_coverage']:.2f}")
        print(f"   Confianza: {result['confidence_score']}")

if __name__ == "__main__":
    try:
        # Probar modelo avanzado
        advanced_model = test_advanced_model()
        
        # Comparar modelos
        compare_models()
        
        # Probar por plusvalía
        test_plusvalia_comparison()
        
        print(f"\n✅ ¡Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
