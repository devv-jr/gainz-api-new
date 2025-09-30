#!/bin/bash

echo "🚀 GAINZ API - Script de Deploy a GitHub"
echo "========================================"

# Verificar si Git está inicializado
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositorio Git..."
    git init
fi

# Verificar configuración de Git
if [ -z "$(git config --global user.name)" ]; then
    echo "⚠️  Configuración de Git requerida"
    read -p "Ingresa tu nombre: " git_name
    read -p "Ingresa tu email: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
fi

# Mostrar estado actual
echo ""
echo "📊 Estado actual del repositorio:"
git status --short

echo ""
echo "📦 Archivos a subir:"
echo "✅ Código fuente completo"
echo "✅ 131 ejercicios en base de datos"
echo "✅ 117 imágenes de ejercicios"
echo "✅ Configuración para Render"
echo "✅ Documentación completa"

echo ""
read -p "¿Continuar con el commit? (y/N): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    # Agregar todos los archivos
    echo "📝 Agregando archivos..."
    git add .
    
    # Crear commit
    echo "💾 Creando commit..."
    git commit -m "feat: Gainz API completa con 131 ejercicios y configuración para producción

- ✅ 131 ejercicios organizados por grupos musculares
- ✅ 117 imágenes PNG de alta calidad
- ✅ Sistema de autenticación JWT completo
- ✅ CRUD de rutinas personalizadas
- ✅ Favoritos y filtros avanzados
- ✅ Configuración para deploy en Render
- ✅ Documentación completa para React Native
- ✅ Scripts de inicialización automática"
    
    echo ""
    echo "✅ Commit creado exitosamente!"
    echo ""
    echo "🌐 Próximos pasos:"
    echo "1. Crear repositorio en GitHub: https://github.com/new"
    echo "2. Ejecutar: git remote add origin https://github.com/TU_USUARIO/gainzapi.git"
    echo "3. Ejecutar: git push -u origin main"
    echo "4. Seguir la guía en DEPLOY.md para Render"
    echo ""
    echo "📚 Ver documentación completa en DEPLOY.md"
else
    echo "❌ Deploy cancelado"
fi