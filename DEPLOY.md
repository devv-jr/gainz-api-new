# 🚀 Guía de Despliegue: GitHub + Render

Esta guía te explica paso a paso cómo subir tu código a GitHub y desplegarlo en Render.

## 📋 Lista de Verificación Pre-Despliegue

✅ **Archivos de configuración creados:**
- `Procfile` - Comando para ejecutar la app en Render
- `runtime.txt` - Versión de Python
- `requirements.txt` - Dependencias actualizadas con PostgreSQL
- `.env.example` - Ejemplo de variables de entorno
- `init_db.py` - Script de inicialización de BD
- `render_deploy.sh` - Script de despliegue
- `.gitignore` - Archivos a ignorar en Git

## 🔧 Paso 1: Preparar el Repositorio GitHub

### 1.1 Inicializar Git (si no está inicializado)

```bash
cd /home/dev/Desktop/gainzapi
git init
```

### 1.2 Configurar Git (primera vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 1.3 Crear repositorio en GitHub

1. Ve a [GitHub.com](https://github.com)
2. Click en "New repository"
3. Nombre: `gainzapi` (o el que prefieras)
4. Descripción: `API REST para app de gimnasio con FastAPI`
5. Selecciona **Public** o **Private**
6. **NO** marques "Add README" (ya tienes uno)
7. Click "Create repository"

### 1.4 Subir código a GitHub

```bash
# Agregar archivos
git add .

# Primer commit
git commit -m "Initial commit: Gainz API with 131 exercises"

# Agregar remote origin (reemplaza con tu URL)
git remote add origin https://github.com/TU_USUARIO/gainzapi.git

# Subir a GitHub
git push -u origin main
```

## 🌐 Paso 2: Desplegar en Render

### 2.1 Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub
3. Autoriza el acceso a tus repositorios

### 2.2 Crear Web Service

1. En Render Dashboard, click **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio `gainzapi`
4. Configura el servicio:

#### **Configuración Básica:**
- **Name**: `gainzapi` (o tu nombre preferido)
- **Region**: `Oregon (US West)` (o más cerca de ti)
- **Branch**: `main`
- **Root Directory**: (dejar vacío)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt && python init_db.py`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### **Plan:**
- Selecciona **"Free"** para comenzar
- (Puedes upgrader después si necesitas más recursos)

### 2.3 Configurar Variables de Entorno

En la sección **"Environment Variables"** agrega:

| Variable | Valor |
|----------|--------|
| `DATABASE_URL` | `postgresql://username:password@hostname/database` |
| `SECRET_KEY` | `tu-clave-secreta-super-segura-de-al-menos-32-caracteres` |
| `DEBUG` | `False` |
| `HOST` | `0.0.0.0` |
| `PORT` | `10000` (Render lo asigna automáticamente) |

### 2.4 Configurar Base de Datos PostgreSQL

#### **Opción A: Base de Datos en Render (Recomendado)**

1. En Render Dashboard, click **"New +"**
2. Selecciona **"PostgreSQL"**
3. Configura:
   - **Name**: `gainzapi-db`
   - **Database**: `gainzapi`
   - **User**: `gainzapi_user`
   - **Region**: Misma que el Web Service
   - **Plan**: **Free** (500MB, suficiente para comenzar)

4. Una vez creada, copia la **"External Database URL"**
5. Pégala en la variable `DATABASE_URL` de tu Web Service

#### **Opción B: Base de Datos Externa**

También puedes usar:
- **Neon** (PostgreSQL gratuito)
- **Supabase** (PostgreSQL con extras)
- **ElephantSQL** (PostgreSQL gratuito)

### 2.5 Desplegar

1. Click **"Create Web Service"**
2. Render automáticamente:
   - Clonará tu repositorio
   - Instalará dependencias
   - Ejecutará `init_db.py` (creará tablas y poblará ejercicios)
   - Iniciará la aplicación

## 📊 Paso 3: Verificar Despliegue

### 3.1 Monitorear el Deploy

En la página de tu servicio verás los logs en tiempo real:

```
==> Building...
==> Installing dependencies from requirements.txt
==> Running python init_db.py
🚀 Inicializando base de datos de producción...
✅ Tablas creadas
📋 Poblando base de datos...
🎉 Inicialización completa
==> Starting server
INFO: Uvicorn running on http://0.0.0.0:10000
```

### 3.2 Probar la API

Una vez desplegada, tu API estará disponible en:
`https://tu-servicio.onrender.com`

Prueba estos endpoints:

- **Health Check**: `https://tu-servicio.onrender.com/health`
- **Documentación**: `https://tu-servicio.onrender.com/docs`
- **API Info**: `https://tu-servicio.onrender.com/`

### 3.3 Probar Funcionalidad Completa

```bash
# Registrar usuario
curl -X POST "https://tu-servicio.onrender.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "test123",
    "full_name": "Test User"
  }'

# Login
curl -X POST "https://tu-servicio.onrender.com/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123"

# Obtener ejercicios (con token del login)
curl -X GET "https://tu-servicio.onrender.com/api/v1/exercises/" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

## 🔄 Paso 4: Actualizaciones Futuras

### 4.1 Actualizar Código

```bash
# Hacer cambios en tu código local
git add .
git commit -m "Descripción de cambios"
git push origin main
```

Render automáticamente detectará los cambios y re-desplegará.

### 4.2 Variables de Entorno

Puedes actualizar variables de entorno en:
`Render Dashboard > Tu Servicio > Environment`

### 4.3 Monitoreo

- **Logs**: Ve logs en tiempo real en Render Dashboard
- **Métricas**: CPU, memoria, requests en la pestaña "Metrics"
- **Alertas**: Configura notificaciones por email

## 🛡️ Paso 5: Configuración de Producción

### 5.1 Dominio Personalizado (Opcional)

1. En Render Dashboard > Settings
2. Agregar tu dominio personalizado
3. Configurar DNS según las instrucciones

### 5.2 SSL/HTTPS

Render proporciona SSL automáticamente para:
- Subdominios `.onrender.com`
- Dominios personalizados

### 5.3 CORS para Producción

En tu `main.py`, actualiza CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-dominio-frontend.com",
        "https://tu-app-movil.com",
        # Agrega tus dominios específicos
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔧 Solución de Problemas

### Problema: Build Falla

**Solución**: Revisa los logs de build en Render Dashboard

### Problema: Base de Datos no se Conecta

**Solución**: 
1. Verifica la `DATABASE_URL` en variables de entorno
2. Asegúrate que la BD PostgreSQL esté corriendo
3. Revisa que los datos de conexión sean correctos

### Problema: Imágenes no Cargan

**Solución**: 
1. Verifica que las imágenes estén en el repositorio
2. Comprueba las rutas en `/images/...`
3. En Render, las imágenes se sirven automáticamente

### Problema: 502 Bad Gateway

**Solución**:
1. Revisa que la app escuche en `0.0.0.0:$PORT`
2. Verifica el `Procfile`
3. Revisa logs de la aplicación

## 📱 Paso 6: Actualizar React Native

Una vez desplegada, actualiza tu config en React Native:

```javascript
// config/api.js
const API_CONFIG = {
  // Para producción
  BASE_URL: 'https://tu-servicio.onrender.com',
  
  // Para desarrollo local (comentar en producción)
  // BASE_URL: 'http://localhost:8000',
  
  ENDPOINTS: {
    AUTH: '/api/v1/auth',
    USERS: '/api/v1/users',
    EXERCISES: '/api/v1/exercises',
    ROUTINES: '/api/v1/routines',
    IMAGES: '/images'
  }
};
```

## 🎉 ¡Listo!

Tu API ahora está desplegada en producción con:

✅ **131 ejercicios** cargados automáticamente
✅ **117 imágenes** servidas estáticamente  
✅ **Base de datos PostgreSQL** en la nube
✅ **SSL/HTTPS** automático
✅ **Documentación** accesible públicamente
✅ **Escalabilidad** automática en Render

### URLs Importantes:

- **API Base**: `https://tu-servicio.onrender.com`
- **Documentación**: `https://tu-servicio.onrender.com/docs`
- **Health Check**: `https://tu-servicio.onrender.com/health`
- **Dashboard Render**: https://dashboard.render.com

¡Tu app de gimnasio ya puede conectarse a una API profesional en producción! 🏋️‍♀️💪