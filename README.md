# Gainz API 💪

API REST completa para gestión de rutinas de gimnasio construida con FastAPI, SQLAlchemy y Python.

## 🚀 Características

- **🔐 Autenticación JWT**: Registro y login seguro de usuarios
- **💪 Base de Datos Completa**: 131+ ejercicios organizados por grupos musculares
- **📋 Rutinas Personalizadas**: Crear, editar, duplicar y compartir rutinas
- **⭐ Ejercicios Favoritos**: Sistema de favoritos para ejercicios
- **🔍 Filtros Avanzados**: Búsqueda por grupo muscular, dificultad, categoría
- **🖼️ Imágenes**: Servir imágenes estáticas de ejercicios (117 imágenes)
- **📚 Documentación Automática**: Swagger UI y ReDoc integrados
- **📱 React Native Ready**: Optimizada para apps móviles

## 📁 Estructura del Proyecto

```
gainzapi/
├── images/                 # Imágenes de ejercicios por grupo muscular
│   ├── abs/
│   ├── biceps/
│   ├── espalda/
│   ├── gemelos/
│   ├── hombros/
│   ├── pectorales/
│   ├── piernas/
│   └── triceps/
├── routers/               # Endpoints organizados
│   ├── auth.py           # Autenticación y autorización
│   ├── users.py          # Gestión de usuarios
│   ├── exercises.py      # CRUD de ejercicios
│   └── routines.py       # CRUD de rutinas
├── main.py               # Aplicación principal FastAPI
├── models.py             # Modelos de base de datos y Pydantic
├── database.py           # Configuración de base de datos
├── auth.py               # Utilidades de autenticación JWT
├── populate_db.py        # Script para poblar la base de datos
├── requirements.txt      # Dependencias Python
└── .env                  # Variables de entorno
```

## 🛠️ Instalación y Configuración

### 1. Clonar y configurar el entorno

```bash
cd /home/dev/Desktop/gainzapi
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Edita el archivo `.env` con tus configuraciones:

```env
DATABASE_URL=sqlite:///./gainzapi.db
SECRET_KEY=tu_clave_secreta_super_segura_aqui_cambiala_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Poblar la base de datos

```bash
python populate_db.py
```

### 4. Ejecutar la aplicación

```bash
python main.py
# O usando uvicorn directamente:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API Endpoints Completos

### 🔐 **Autenticación**
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/register` | Registrar nuevo usuario | ❌ |
| `POST` | `/api/v1/auth/login` | Login (devuelve JWT token) | ❌ |
| `GET` | `/api/v1/auth/me` | Obtener usuario actual | ✅ |
| `POST` | `/api/v1/auth/refresh-token` | Renovar token de acceso | ✅ |

### 👤 **Usuarios**
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/users/profile` | Obtener perfil del usuario | ✅ |
| `PUT` | `/api/v1/users/profile` | Actualizar perfil | ✅ |
| `DELETE` | `/api/v1/users/profile` | Eliminar cuenta | ✅ |

### 💪 **Ejercicios**
| Método | Endpoint | Descripción | Parámetros | Autenticación |
|--------|----------|-------------|------------|---------------|
| `GET` | `/api/v1/exercises/` | Listar todos los ejercicios | `grupo_muscular`, `nivel_dificultad`, `search`, `skip`, `limit` | ✅ |
| `GET` | `/api/v1/exercises/grupos-musculares` | Lista de grupos musculares | - | ✅ |
| `GET` | `/api/v1/exercises/grupo/{grupo_muscular}` | Ejercicios por grupo | `skip`, `limit` | ✅ |
| `GET` | `/api/v1/exercises/{exercise_id}` | Obtener ejercicio específico | - | ✅ |
| `GET` | `/api/v1/exercises/favoritos` | Ejercicios favoritos del usuario | - | ✅ |
| `POST` | `/api/v1/exercises/favoritos/{exercise_id}` | Agregar ejercicio a favoritos | - | ✅ |
| `DELETE` | `/api/v1/exercises/favoritos/{exercise_id}` | Remover de favoritos | - | ✅ |

### 📋 **Rutinas**
| Método | Endpoint | Descripción | Parámetros | Autenticación |
|--------|----------|-------------|------------|---------------|
| `GET` | `/api/v1/routines/` | Listar rutinas (propias + públicas) | `categoria`, `nivel_dificultad`, `is_public`, `search`, `skip`, `limit` | ✅ |
| `GET` | `/api/v1/routines/mis-rutinas` | Solo rutinas del usuario | - | ✅ |
| `GET` | `/api/v1/routines/categorias` | Lista de categorías | - | ✅ |
| `GET` | `/api/v1/routines/plantillas` | Rutinas plantilla predefinidas | `categoria`, `nivel_dificultad` | ✅ |
| `POST` | `/api/v1/routines/` | Crear nueva rutina | - | ✅ |
| `GET` | `/api/v1/routines/{rutina_id}` | Obtener rutina específica | - | ✅ |
| `PUT` | `/api/v1/routines/{rutina_id}` | Actualizar rutina (solo propietario) | - | ✅ |
| `DELETE` | `/api/v1/routines/{rutina_id}` | Eliminar rutina (solo propietario) | - | ✅ |
| `POST` | `/api/v1/routines/{rutina_id}/duplicar` | Duplicar rutina (crear copia) | - | ✅ |

### 🔧 **Gestión de Series en Rutinas**
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/routines/{rutina_id}/series` | Agregar ejercicio a rutina | ✅ |
| `PUT` | `/api/v1/routines/{rutina_id}/series/{serie_id}` | Actualizar serie en rutina | ✅ |
| `DELETE` | `/api/v1/routines/{rutina_id}/series/{serie_id}` | Remover ejercicio de rutina | ✅ |

### 🖼️ **Imágenes Estáticas**
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `GET` | `/images/{grupo_muscular}/{imagen.png}` | Servir imagen de ejercicio | ❌ |

**Ejemplos de URLs de imágenes:**
- `/images/pectorales/press-banca.png`
- `/images/biceps/curl-con-barra.png`
- `/images/piernas/sentadilla.png`

## 📊 Base de Datos de Ejercicios

La API incluye **131 ejercicios completos** distribuidos en 8 grupos musculares:

| Grupo Muscular | Ejercicios | Ejemplos |
|----------------|------------|----------|
| **ABS** | 13 | Plancha, Crunch, Abdominales con cuerda |
| **BÍCEPS** | 16 | Curl con barra, Curl martillo, Curl predicador |
| **ESPALDA** | 23 | Dominadas, Peso muerto, Remo con barra |
| **GEMELOS** | 4 | Elevación de gemelos de pie/sentado |
| **HOMBROS** | 19 | Press militar, Elevaciones laterales/frontales |
| **PECTORALES** | 12 | Press banca, Aperturas, Flexiones |
| **PIERNAS** | 29 | Sentadillas, Peso muerto rumano, Prensa |
| **TRÍCEPS** | 15 | Extensiones, Fondos, Press francés |

### 🖼️ Imágenes de Ejercicios
- **117 imágenes PNG** de alta calidad
- Organizadas por grupo muscular
- URLs accesibles: `/images/{grupo}/{ejercicio}.png`

## 📊 Ejemplo de Uso

### Registrar Usuario
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "username": "miusuario",
    "password": "mipassword123",
    "full_name": "Mi Nombre"
  }'
```

### Crear Rutina
```bash
curl -X POST "http://localhost:8000/api/v1/routines/" \
  -H "Authorization: Bearer tu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Mi Rutina Push",
    "descripcion": "Rutina de empuje para pecho y hombros",
    "categoria": "hipertrofia",
    "nivel_dificultad": "intermedio",
    "series": [
      {
        "ejercicio_id": 1,
        "orden": 1,
        "series": 4,
        "repeticiones_min": 8,
        "repeticiones_max": 10,
        "tiempo_descanso": 90
      }
    ]
  }'
```

## 📚 Documentación

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Desarrollo

### Estructura de Modelos

**Usuario**: Email, username, contraseña, rutinas creadas, ejercicios favoritos

**Ejercicio**: Nombre, grupo muscular, descripción, instrucciones, nivel, equipo, imagen

**Rutina**: Nombre, descripción, categoría, dificultad, series de ejercicios

**SerieEjercicio**: Ejercicio específico dentro de una rutina con series, repeticiones, peso

### Base de Datos

Por defecto usa SQLite para desarrollo. Para producción, configura PostgreSQL en el archivo `.env`:

```env
DATABASE_URL=postgresql://usuario:password@localhost/gainzapi
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribuir

1. Fork del proyecto
2. Crear branch para feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

# 📱 Integración con React Native

Esta sección te explica paso a paso cómo integrar Gainz API con tu aplicación React Native.

## 🛠️ Configuración Inicial

### 1. **Configurar Base URL**

Crea un archivo `config/api.js` en tu proyecto React Native:

```javascript
// config/api.js
const API_CONFIG = {
  // Para desarrollo local
  BASE_URL: 'http://10.0.2.2:8000', // Android Emulator
  // BASE_URL: 'http://localhost:8000', // iOS Simulator
  // BASE_URL: 'http://192.168.1.XXX:8000', // Tu IP local para dispositivos físicos
  
  // Para producción
  // BASE_URL: 'https://tu-dominio.com',
  
  ENDPOINTS: {
    AUTH: '/api/v1/auth',
    USERS: '/api/v1/users',
    EXERCISES: '/api/v1/exercises',
    ROUTINES: '/api/v1/routines',
    IMAGES: '/images'
  }
};

export default API_CONFIG;
```

### 2. **Instalar Dependencias**

```bash
npm install @react-native-async-storage/async-storage
# o
yarn add @react-native-async-storage/async-storage
```

## 🔐 Sistema de Autenticación

### **AuthService.js**

```javascript
// services/AuthService.js
import AsyncStorage from '@react-native-async-storage/async-storage';
import API_CONFIG from '../config/api';

class AuthService {
  async login(username, password) {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
      });

      if (response.ok) {
        const data = await response.json();
        await AsyncStorage.setItem('access_token', data.access_token);
        return { success: true, data };
      } else {
        const error = await response.json();
        return { success: false, error: error.detail };
      }
    } catch (error) {
      return { success: false, error: 'Error de conexión' };
    }
  }

  async register(userData) {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      });

      if (response.ok) {
        const data = await response.json();
        return { success: true, data };
      } else {
        const error = await response.json();
        return { success: false, error: error.detail };
      }
    } catch (error) {
      return { success: false, error: 'Error de conexión' };
    }
  }

  async logout() {
    await AsyncStorage.removeItem('access_token');
  }

  async getToken() {
    return await AsyncStorage.getItem('access_token');
  }

  async getCurrentUser() {
    try {
      const token = await this.getToken();
      if (!token) return null;

      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH}/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      return null;
    }
  }
}

export default new AuthService();
```

### **Hook de Autenticación**

```javascript
// hooks/useAuth.js
import { useState, useEffect, createContext, useContext } from 'react';
import AuthService from '../services/AuthService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthState();
  }, []);

  const checkAuthState = async () => {
    const currentUser = await AuthService.getCurrentUser();
    setUser(currentUser);
    setLoading(false);
  };

  const login = async (username, password) => {
    const result = await AuthService.login(username, password);
    if (result.success) {
      const currentUser = await AuthService.getCurrentUser();
      setUser(currentUser);
    }
    return result;
  };

  const register = async (userData) => {
    return await AuthService.register(userData);
  };

  const logout = async () => {
    await AuthService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

## 💪 Servicio de Ejercicios

### **ExerciseService.js**

```javascript
// services/ExerciseService.js
import AuthService from './AuthService';
import API_CONFIG from '../config/api';

class ExerciseService {
  async makeAuthenticatedRequest(endpoint, options = {}) {
    const token = await AuthService.getToken();
    
    return fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
  }

  // Obtener todos los ejercicios con filtros
  async getExercises(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.grupo_muscular) params.append('grupo_muscular', filters.grupo_muscular);
    if (filters.nivel_dificultad) params.append('nivel_dificultad', filters.nivel_dificultad);
    if (filters.search) params.append('search', filters.search);
    if (filters.skip) params.append('skip', filters.skip);
    if (filters.limit) params.append('limit', filters.limit);

    const queryString = params.toString();
    const endpoint = `${API_CONFIG.ENDPOINTS.EXERCISES}${queryString ? `?${queryString}` : ''}`;
    
    try {
      const response = await this.makeAuthenticatedRequest(endpoint);
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener ejercicios');
    } catch (error) {
      throw error;
    }
  }

  // Obtener ejercicios por grupo muscular
  async getExercisesByGroup(groupName, skip = 0, limit = 50) {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.EXERCISES}/grupo/${groupName}?skip=${skip}&limit=${limit}`
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener ejercicios del grupo');
    } catch (error) {
      throw error;
    }
  }

  // Obtener ejercicios favoritos
  async getFavoriteExercises() {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.EXERCISES}/favoritos`
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener ejercicios favoritos');
    } catch (error) {
      throw error;
    }
  }

  // Agregar ejercicio a favoritos
  async addToFavorites(exerciseId) {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.EXERCISES}/favoritos/${exerciseId}`,
        { method: 'POST' }
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al agregar a favoritos');
    } catch (error) {
      throw error;
    }
  }

  // Remover ejercicio de favoritos
  async removeFromFavorites(exerciseId) {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.EXERCISES}/favoritos/${exerciseId}`,
        { method: 'DELETE' }
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al remover de favoritos');
    } catch (error) {
      throw error;
    }
  }

  // Obtener URL de imagen de ejercicio
  getExerciseImageUrl(imagePath) {
    // imagePath viene como "/images/pectorales/press-banca.png"
    return `${API_CONFIG.BASE_URL}${imagePath}`;
  }

  // Obtener grupos musculares disponibles
  async getMuscleGroups() {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.EXERCISES}/grupos-musculares`
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener grupos musculares');
    } catch (error) {
      throw error;
    }
  }
}

export default new ExerciseService();
```

## 📋 Servicio de Rutinas

### **RoutineService.js**

```javascript
// services/RoutineService.js
import AuthService from './AuthService';
import API_CONFIG from '../config/api';

class RoutineService {
  async makeAuthenticatedRequest(endpoint, options = {}) {
    const token = await AuthService.getToken();
    
    return fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
  }

  // Obtener rutinas con filtros
  async getRoutines(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.categoria) params.append('categoria', filters.categoria);
    if (filters.nivel_dificultad) params.append('nivel_dificultad', filters.nivel_dificultad);
    if (filters.is_public !== undefined) params.append('is_public', filters.is_public);
    if (filters.search) params.append('search', filters.search);
    if (filters.skip) params.append('skip', filters.skip);
    if (filters.limit) params.append('limit', filters.limit);

    const queryString = params.toString();
    const endpoint = `${API_CONFIG.ENDPOINTS.ROUTINES}${queryString ? `?${queryString}` : ''}`;
    
    try {
      const response = await this.makeAuthenticatedRequest(endpoint);
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener rutinas');
    } catch (error) {
      throw error;
    }
  }

  // Obtener mis rutinas
  async getMyRoutines() {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.ROUTINES}/mis-rutinas`
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener mis rutinas');
    } catch (error) {
      throw error;
    }
  }

  // Crear nueva rutina
  async createRoutine(routineData) {
    try {
      const response = await this.makeAuthenticatedRequest(
        API_CONFIG.ENDPOINTS.ROUTINES,
        {
          method: 'POST',
          body: JSON.stringify(routineData),
        }
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al crear rutina');
    } catch (error) {
      throw error;
    }
  }

  // Obtener rutina específica
  async getRoutine(routineId) {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.ROUTINES}/${routineId}`
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener rutina');
    } catch (error) {
      throw error;
    }
  }

  // Duplicar rutina
  async duplicateRoutine(routineId) {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.ROUTINES}/${routineId}/duplicar`,
        { method: 'POST' }
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al duplicar rutina');
    } catch (error) {
      throw error;
    }
  }

  // Obtener categorías de rutinas
  async getRoutineCategories() {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${API_CONFIG.ENDPOINTS.ROUTINES}/categorias`
      );
      if (response.ok) {
        return await response.json();
      }
      throw new Error('Error al obtener categorías');
    } catch (error) {
      throw error;
    }
  }
}

export default new RoutineService();
```

## 🎨 Componentes de Ejemplo

### **Componente de Ejercicio**

```javascript
// components/ExerciseCard.js
import React, { useState } from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';
import ExerciseService from '../services/ExerciseService';

const ExerciseCard = ({ exercise, onFavoriteToggle }) => {
  const [isFavorite, setIsFavorite] = useState(false);

  const toggleFavorite = async () => {
    try {
      if (isFavorite) {
        await ExerciseService.removeFromFavorites(exercise.id);
      } else {
        await ExerciseService.addToFavorites(exercise.id);
      }
      setIsFavorite(!isFavorite);
      onFavoriteToggle && onFavoriteToggle(exercise.id, !isFavorite);
    } catch (error) {
      console.error('Error al cambiar favorito:', error);
    }
  };

  return (
    <View style={styles.card}>
      <Image 
        source={{ uri: ExerciseService.getExerciseImageUrl(exercise.imagen_url) }}
        style={styles.image}
        resizeMode="cover"
      />
      <View style={styles.content}>
        <Text style={styles.name}>{exercise.nombre}</Text>
        <Text style={styles.group}>{exercise.grupo_muscular.toUpperCase()}</Text>
        <Text style={styles.description}>{exercise.descripcion}</Text>
        <View style={styles.details}>
          <Text style={styles.difficulty}>Nivel: {exercise.nivel_dificultad}</Text>
          <Text style={styles.equipment}>Equipo: {exercise.equipo_necesario}</Text>
        </View>
        <TouchableOpacity 
          style={[styles.favoriteButton, isFavorite && styles.favoriteActive]}
          onPress={toggleFavorite}
        >
          <Text style={styles.favoriteText}>
            {isFavorite ? '❤️ Favorito' : '🤍 Agregar a favoritos'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  image: {
    width: '100%',
    height: 200,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  content: {
    padding: 16,
  },
  name: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  group: {
    fontSize: 12,
    color: '#666',
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: '#555',
    lineHeight: 20,
    marginBottom: 12,
  },
  details: {
    marginBottom: 12,
  },
  difficulty: {
    fontSize: 12,
    color: '#666',
    marginBottom: 2,
  },
  equipment: {
    fontSize: 12,
    color: '#666',
  },
  favoriteButton: {
    backgroundColor: '#f0f0f0',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  favoriteActive: {
    backgroundColor: '#ffebee',
  },
  favoriteText: {
    fontSize: 14,
    fontWeight: '500',
  },
});

export default ExerciseCard;
```

### **Hook para Ejercicios**

```javascript
// hooks/useExercises.js
import { useState, useEffect } from 'react';
import ExerciseService from '../services/ExerciseService';

export const useExercises = (filters = {}) => {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchExercises = async () => {
    try {
      setLoading(true);
      const data = await ExerciseService.getExercises(filters);
      setExercises(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExercises();
  }, [JSON.stringify(filters)]);

  const refetch = () => fetchExercises();

  return { exercises, loading, error, refetch };
};

export const useExercisesByGroup = (groupName) => {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExercises = async () => {
      try {
        setLoading(true);
        const data = await ExerciseService.getExercisesByGroup(groupName);
        setExercises(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (groupName) {
      fetchExercises();
    }
  }, [groupName]);

  return { exercises, loading, error };
};
```

## 📋 Esquemas de Datos

### **Ejercicio**
```javascript
const ExerciseSchema = {
  id: 1,
  nombre: "Press Banca",
  grupo_muscular: "pectorales",
  descripcion: "Ejercicio fundamental para el desarrollo del pecho",
  instrucciones: "Acostado en banco, baja la barra al pecho y presiona hacia arriba",
  nivel_dificultad: "intermedio", // "principiante" | "intermedio" | "avanzado"
  equipo_necesario: "Banco, barra, discos",
  musculos_secundarios: "tríceps, deltoides anterior",
  imagen_url: "/images/pectorales/press-banca.png",
  is_active: true,
  created_at: "2025-09-29T10:00:00Z"
};
```

### **Rutina**
```javascript
const RoutineSchema = {
  id: 1,
  nombre: "Rutina Push - Pecho, Hombros, Tríceps",
  descripcion: "Rutina de entrenamiento enfocada en músculos de empuje",
  categoria: "hipertrofia", // "fuerza" | "hipertrofia" | "resistencia" | "definicion" | "funcional"
  duracion_estimada: 60, // minutos
  nivel_dificultad: "intermedio",
  is_public: true,
  is_template: false,
  owner_id: 1,
  created_at: "2025-09-29T10:00:00Z",
  updated_at: "2025-09-29T10:00:00Z",
  series: [
    {
      id: 1,
      rutina_id: 1,
      ejercicio_id: 15,
      orden: 1,
      series: 4,
      repeticiones_min: 8,
      repeticiones_max: 10,
      peso: 80.0, // opcional
      tiempo_descanso: 90, // segundos
      notas: "Mantener técnica correcta", // opcional
      ejercicio: ExerciseSchema // objeto ejercicio completo
    }
  ],
  owner: {
    id: 1,
    username: "usuario",
    full_name: "Usuario Ejemplo"
  }
};
```

## 🚀 Configuración de Red

### **Para Android Emulator:**
```javascript
const BASE_URL = 'http://10.0.2.2:8000';
```

### **Para iOS Simulator:**
```javascript
const BASE_URL = 'http://localhost:8000';
```

### **Para Dispositivos Físicos:**
```javascript
// Usa tu IP local (puedes obtenerla con ipconfig/ifconfig)
const BASE_URL = 'http://192.168.1.XXX:8000';
```

### **Network Security Config (Android)**

Si usas HTTP en desarrollo, agrega esto a `android/app/src/main/res/xml/network_security_config.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">192.168.1.XXX</domain>
    </domain-config>
</network-security-config>
```

Y en `android/app/src/main/AndroidManifest.xml`:

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```

## 🔍 Ejemplos de Uso Prácticos

### **1. Pantalla de Login**

```javascript
// screens/LoginScreen.js
import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, Text, Alert } from 'react-native';
import { useAuth } from '../hooks/useAuth';

const LoginScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Por favor completa todos los campos');
      return;
    }

    setLoading(true);
    const result = await login(username, password);
    setLoading(false);

    if (result.success) {
      navigation.replace('Home');
    } else {
      Alert.alert('Error', result.error);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput
        placeholder="Usuario o Email"
        value={username}
        onChangeText={setUsername}
        style={{ borderWidth: 1, padding: 15, marginBottom: 15, borderRadius: 8 }}
      />
      <TextInput
        placeholder="Contraseña"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={{ borderWidth: 1, padding: 15, marginBottom: 20, borderRadius: 8 }}
      />
      <TouchableOpacity
        onPress={handleLogin}
        disabled={loading}
        style={{ 
          backgroundColor: '#007AFF', 
          padding: 15, 
          borderRadius: 8, 
          alignItems: 'center' 
        }}
      >
        <Text style={{ color: 'white', fontWeight: 'bold' }}>
          {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

export default LoginScreen;
```

### **2. Lista de Ejercicios por Grupo**

```javascript
// screens/ExerciseListScreen.js
import React from 'react';
import { FlatList, View, Text, ActivityIndicator } from 'react-native';
import { useExercisesByGroup } from '../hooks/useExercises';
import ExerciseCard from '../components/ExerciseCard';

const ExerciseListScreen = ({ route }) => {
  const { groupName } = route.params;
  const { exercises, loading, error } = useExercisesByGroup(groupName);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={{ marginTop: 10 }}>Cargando ejercicios...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Text style={{ color: 'red' }}>Error: {error}</Text>
      </View>
    );
  }

  return (
    <FlatList
      data={exercises}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => <ExerciseCard exercise={item} />}
      contentContainerStyle={{ padding: 16 }}
      showsVerticalScrollIndicator={false}
    />
  );
};

export default ExerciseListScreen;
```

### **3. Crear Rutina**

```javascript
// screens/CreateRoutineScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import RoutineService from '../services/RoutineService';

const CreateRoutineScreen = ({ navigation }) => {
  const [routineName, setRoutineName] = useState('');
  const [description, setDescription] = useState('');
  const [categoria, setCategoria] = useState('hipertrofia');
  const [loading, setLoading] = useState(false);

  const handleCreateRoutine = async () => {
    if (!routineName.trim()) {
      Alert.alert('Error', 'El nombre de la rutina es obligatorio');
      return;
    }

    setLoading(true);
    try {
      const routineData = {
        nombre: routineName,
        descripcion: description,
        categoria: categoria,
        nivel_dificultad: 'intermedio',
        is_public: false,
        series: [] // Empezar con rutina vacía
      };

      const newRoutine = await RoutineService.createRoutine(routineData);
      Alert.alert('Éxito', 'Rutina creada exitosamente', [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 20 }}>
        Crear Nueva Rutina
      </Text>
      
      <TextInput
        placeholder="Nombre de la rutina"
        value={routineName}
        onChangeText={setRoutineName}
        style={{ borderWidth: 1, padding: 15, marginBottom: 15, borderRadius: 8 }}
      />
      
      <TextInput
        placeholder="Descripción (opcional)"
        value={description}
        onChangeText={setDescription}
        multiline
        numberOfLines={3}
        style={{ borderWidth: 1, padding: 15, marginBottom: 20, borderRadius: 8 }}
      />
      
      <TouchableOpacity
        onPress={handleCreateRoutine}
        disabled={loading}
        style={{ 
          backgroundColor: '#007AFF', 
          padding: 15, 
          borderRadius: 8, 
          alignItems: 'center' 
        }}
      >
        <Text style={{ color: 'white', fontWeight: 'bold' }}>
          {loading ? 'Creando...' : 'Crear Rutina'}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

export default CreateRoutineScreen;
```

## 🐛 Solución de Problemas Comunes

### **1. Error de Conexión**
```javascript
// Verificar conectividad
const checkConnection = async () => {
  try {
    const response = await fetch(`${API_CONFIG.BASE_URL}/health`);
    console.log('API Status:', response.status);
  } catch (error) {
    console.log('Connection Error:', error.message);
  }
};
```

### **2. Token Expirado**
```javascript
// En tu interceptor de errores
const handleApiError = (response) => {
  if (response.status === 401) {
    // Token expirado, hacer logout
    AuthService.logout();
    // Redirigir a login
  }
};
```

### **3. Manejo de Imágenes**
```javascript
// Componente para imágenes con fallback
const ExerciseImage = ({ imageUrl, style }) => {
  const [imageError, setImageError] = useState(false);

  return (
    <Image
      source={
        imageError 
          ? require('../assets/placeholder-exercise.png')
          : { uri: ExerciseService.getExerciseImageUrl(imageUrl) }
      }
      style={style}
      onError={() => setImageError(true)}
    />
  );
};
```

## 📋 Lista de Verificación

- [ ] ✅ Configurar BASE_URL correcta para tu entorno
- [ ] ✅ Instalar AsyncStorage para tokens
- [ ] ✅ Implementar AuthService y AuthProvider
- [ ] ✅ Crear servicios para Exercises y Routines
- [ ] ✅ Configurar network security (Android)
- [ ] ✅ Manejar estados de loading y error
- [ ] ✅ Implementar refresh de datos
- [ ] ✅ Agregar manejo de imágenes con fallback
- [ ] ✅ Probar en emulador y dispositivo físico

¡Tu integración con React Native está lista! 🚀💪

---

## 🛠️ Desarrollo y Despliegue

### **Ejecutar la API Localmente**

```bash
# 1. Clonar y configurar
cd /home/dev/Desktop/gainzapi
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
# Editar .env con tus configuraciones

# 4. Poblar base de datos
python populate_all_exercises.py

# 5. Ejecutar API
python main.py
# O usando el script automático:
./run.sh
```

### **Documentación de la API**

Una vez ejecutándose, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### **Base de Datos**

- **Desarrollo**: SQLite (`gainzapi.db`)
- **Producción**: Configura PostgreSQL en `.env`:
  ```env
  DATABASE_URL=postgresql://usuario:password@localhost/gainzapi
  ```

### **Estructura de Archivos del Proyecto**

```
gainzapi/
├── 📱 main.py                    # Aplicación FastAPI principal
├── 🗄️ models.py                  # Modelos SQLAlchemy y Pydantic
├── 🔗 database.py                # Configuración de base de datos
├── 🔐 auth.py                    # Utilidades JWT
├── 📋 requirements.txt           # Dependencias Python
├── ⚙️ .env                       # Variables de entorno
├── 🖼️ images/                    # 117 imágenes de ejercicios
│   ├── abs/
│   ├── biceps/
│   ├── espalda/
│   ├── gemelos/
│   ├── hombros/
│   ├── pectorales/
│   ├── piernas/
│   └── triceps/
├── 📡 routers/                   # Endpoints organizados
│   ├── auth.py                  # Autenticación
│   ├── users.py                 # Gestión de usuarios
│   ├── exercises.py             # CRUD de ejercicios
│   └── routines.py              # CRUD de rutinas
├── 🚀 populate_all_exercises.py  # Script poblador completo
├── 🧪 examples.py                # Ejemplos de uso de la API
└── 📚 README.md                  # Esta documentación
```

## 💡 Consejos Adicionales

### **Optimización de Rendimiento**
- Usa paginación en listas largas (`skip` y `limit`)
- Implementa caché local para ejercicios en React Native
- Comprime imágenes para mejor rendimiento en móvil

### **Seguridad**
- Siempre usa HTTPS en producción
- Configura CORS adecuadamente
- Rota tokens JWT regularmente
- Valida todas las entradas del usuario

### **Monitoreo**
- Implementa logging para errores
- Monitorea tiempo de respuesta de la API
- Configura alertas para errores 500

## 🤝 Contribuir

1. **Fork** del proyecto
2. **Crear branch** para feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** de cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Abrir Pull Request**

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**.

---

**Desarrollado con ❤️ para la comunidad fitness 💪**

### 🆘 Soporte

¿Necesitas ayuda? 

- 📚 **Documentación**: http://localhost:8000/docs
- 🐛 **Issues**: Reporta problemas en GitHub
- 💬 **Discusión**: Únete a la comunidad

### 📊 Estadísticas del Proyecto

- ✅ **131 ejercicios** incluidos
- ✅ **117 imágenes** de alta calidad
- ✅ **8 grupos musculares** organizados
- ✅ **API REST completa** con autenticación
- ✅ **React Native ready** con ejemplos completos
- ✅ **Documentación interactiva** con Swagger

¡Disfruta construyendo tu app de fitness! 🏋️‍♀️🚀