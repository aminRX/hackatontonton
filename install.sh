#!/bin/bash

# Web App Experience Service - Script de instalación automática
# Este script instala y configura todo lo necesario para ejecutar el servicio

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Header del script
echo "================================================================"
print_header "🚀 Web App Experience Service - Instalación Automática"
echo "================================================================"
echo

# 1. Verificar Python
print_message "Verificando Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d" " -f2)
    print_message "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python3 no está instalado. Por favor instala Python 3.8.1 o superior"
    exit 1
fi

# 2. Verificar/Instalar Poetry
print_message "Verificando Poetry..."
if command_exists poetry; then
    POETRY_VERSION=$(poetry --version 2>&1)
    print_message "Poetry ya está instalado: $POETRY_VERSION"
else
    print_warning "Poetry no encontrado. Instalando Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Agregar Poetry al PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    if command_exists poetry; then
        print_message "✅ Poetry instalado correctamente"
    else
        print_error "Error instalando Poetry. Por favor instala manualmente: https://python-poetry.org/docs/#installation"
        exit 1
    fi
fi

# 3. Instalar dependencias del proyecto
print_message "Instalando dependencias del proyecto..."
poetry install

print_message "✅ Dependencias instaladas correctamente"

# 4. Verificar que la aplicación se puede importar
print_message "Verificando la aplicación..."
if poetry run python -c "from app.main import app; print('App loaded successfully')" 2>/dev/null; then
    print_message "✅ Aplicación verificada correctamente"
else
    print_error "Error al verificar la aplicación"
    exit 1
fi

# 5. Crear script de inicio
print_message "Creando script de inicio..."
cat > start_service.sh << 'EOF'
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
EOF

chmod +x start_service.sh
print_message "✅ Script de inicio creado: start_service.sh"

# 6. Crear script de pruebas
print_message "Creando script de pruebas..."
cat > run_tests.sh << 'EOF'
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
EOF

chmod +x run_tests.sh
print_message "✅ Script de pruebas creado: run_tests.sh"

# 7. Crear script para detener el servicio
print_message "Creando script para detener el servicio..."
cat > stop_service.sh << 'EOF'
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
EOF

chmod +x stop_service.sh
print_message "✅ Script de parada creado: stop_service.sh"

# 8. Crear archivo de configuración de entorno (opcional)
print_message "Creando archivo de configuración de entorno..."
cat > .env.example << 'EOF'
# Configuración del Web App Experience Service

# Puerto del servicio (por defecto: 8000)
PORT=8000

# Host del servicio (por defecto: 0.0.0.0)
HOST=0.0.0.0

# Modo de desarrollo (por defecto: true)
DEBUG=true

# Nivel de log (por defecto: info)
LOG_LEVEL=info
EOF

print_message "✅ Archivo de configuración de ejemplo creado: .env.example"

# 9. Actualizar .gitignore para incluir los nuevos scripts
print_message "Actualizando .gitignore..."
if ! grep -q "# Scripts de instalación" .gitignore; then
    cat >> .gitignore << 'EOF'

# Scripts de instalación y configuración local
.env
EOF
fi

# 10. Resumen final
echo
echo "================================================================"
print_header "✅ ¡Instalación completada exitosamente!"
echo "================================================================"
echo
print_message "Scripts creados:"
echo "  🚀 start_service.sh  - Inicia el servicio"
echo "  🧪 run_tests.sh      - Ejecuta las pruebas"
echo "  🛑 stop_service.sh   - Detiene el servicio"
echo
print_message "Para empezar a usar el servicio:"
echo "  1. ./start_service.sh"
echo "  2. En otra terminal: ./run_tests.sh"
echo
print_message "URLs del servicio una vez iniciado:"
echo "  🌐 API: http://localhost:8000"
echo "  📚 Docs: http://localhost:8000/docs"
echo "  📖 ReDoc: http://localhost:8000/redoc"
echo
print_message "Para detener el servicio:"
echo "  ./stop_service.sh"
echo
echo "================================================================"
print_header "🎉 ¡Listo para usar!"
echo "================================================================"
