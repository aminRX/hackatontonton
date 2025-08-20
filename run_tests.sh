#!/bin/bash

# Script para ejecutar las pruebas del servicio

# Configurar PATH para Poetry si es necesario
export PATH="$HOME/.local/bin:$PATH"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🧪 Ejecutando pruebas del Web App Experience Service...${NC}"
echo "================================================================"

# Verificar si el servicio está corriendo
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Servicio detectado en http://localhost:8000${NC}"
    echo
    poetry run python test_service.py
else
    echo -e "${YELLOW}⚠️  El servicio no está corriendo en http://localhost:8000${NC}"
    echo "Por favor, inicia el servicio primero ejecutando: ./start_service.sh"
    echo
    echo "Alternativamente, puedes iniciar el servicio en background y ejecutar las pruebas:"
    echo "1. ./start_service.sh &"
    echo "2. sleep 3"
    echo "3. ./run_tests.sh"
    exit 1
fi
