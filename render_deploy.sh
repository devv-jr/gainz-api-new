# Render Deploy Script
echo "🚀 Iniciando despliegue en Render..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Inicializar base de datos
echo "🗄️ Inicializando base de datos..."
python init_db.py

echo "✅ Despliegue completado"