#!/bin/bash

# Script para ejecutar la API de Gainz

echo "🏋️ Iniciando Gainz API..."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Verificar si la base de datos existe
if [ ! -f "gainzapi.db" ]; then
    echo "🗄️ Base de datos no encontrada. Poblando..."
    python populate_db.py
fi

# Ejecutar la aplicación
echo "🚀 Ejecutando Gainz API en http://localhost:8000"
echo "📚 Documentación disponible en:"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Presiona Ctrl+C para detener la aplicación"

python main.py