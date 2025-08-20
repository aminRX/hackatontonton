#!/usr/bin/env python3
"""
Script de ejemplo para probar el servicio web-and-app-experience
"""

import requests
import json

# URL del servicio
BASE_URL = "http://localhost:8000"

def test_root():
    """Prueba el endpoint raíz"""
    print("=== Probando endpoint raíz ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_health():
    """Prueba el endpoint de health check"""
    print("=== Probando health check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_web_app_experience(wifi, device):
    """Prueba el endpoint web-and-app-experience"""
    print(f"=== Probando web-and-app-experience (wifi={wifi}, device={device}) ===")
    
    params = {
        "wifi": wifi,
        "device": device
    }
    
    response = requests.get(
        f"{BASE_URL}/web-and-app-experience",
        params=params
    )
    
    print(f"Status: {response.status_code}")
    print(f"URL: {response.url}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Función principal"""
    print("🚀 Probando Web App Experience Service")
    print("=" * 50)
    
    # Probar endpoints básicos
    test_root()
    test_health()
    
    # Probar casos válidos
    test_web_app_experience(True, "android")
    test_web_app_experience(False, "ios")
    test_web_app_experience(True, "ios")
    test_web_app_experience(False, "android")
    
    # Probar caso inválido
    print("=== Probando caso inválido ===")
    try:
        params = {"wifi": True, "device": "windows"}
        response = requests.get(
            f"{BASE_URL}/web-and-app-experience",
            params=params
        )
        print(f"Status: {response.status_code}")
        print(f"URL: {response.url}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    print("✅ Pruebas completadas!")

if __name__ == "__main__":
    main()
