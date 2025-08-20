#!/bin/bash

# Script para detener el Web App Experience Service

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🛑 Deteniendo Web App Experience Service...${NC}"

# Buscar y terminar procesos de uvicorn
PIDS=$(pgrep -f "uvicorn app.main:app")

if [ -n "$PIDS" ]; then
    echo "Terminando procesos: $PIDS"
    kill $PIDS
    echo -e "${GREEN}✅ Servicio detenido${NC}"
else
    echo -e "${YELLOW}⚠️  No se encontraron procesos del servicio corriendo${NC}"
fi
