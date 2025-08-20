#!/bin/bash

# Script para iniciar el Web App Experience Service

# Configurar PATH para Poetry si es necesario
export PATH="$HOME/.local/bin:$PATH"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Iniciando Web App Experience Service...${NC}"
echo "================================================================"
echo -e "${GREEN}Servicio disponible en:${NC} http://localhost:8000"
echo -e "${GREEN}Documentación Swagger:${NC} http://localhost:8000/docs"
echo -e "${GREEN}Documentación ReDoc:${NC} http://localhost:8000/redoc"
echo "================================================================"
echo

# Iniciar el servicio
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
