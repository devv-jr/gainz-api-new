"""
Ejemplos de uso de la API Gainz
"""
import requests
import json

# Configuración
BASE_URL = "http://localhost:8000/api/v1"

def register_user():
    """Ejemplo: Registrar usuario"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Usuario de Prueba"
    }
    
    response = requests.post(url, json=data)
    print("📝 Registro de usuario:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def login_user():
    """Ejemplo: Login de usuario"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(url, data=data)
    print("\n🔐 Login de usuario:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def get_exercises(token):
    """Ejemplo: Obtener ejercicios"""
    url = f"{BASE_URL}/exercises/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print("\n💪 Lista de ejercicios:")
    print(f"Status: {response.status_code}")
    exercises = response.json()
    print(f"Total ejercicios: {len(exercises)}")
    
    # Mostrar los primeros 3 ejercicios
    for i, exercise in enumerate(exercises[:3]):
        print(f"  {i+1}. {exercise['nombre']} ({exercise['grupo_muscular']})")
    
    return exercises

def get_exercises_by_group(token, grupo="pectorales"):
    """Ejemplo: Obtener ejercicios por grupo muscular"""
    url = f"{BASE_URL}/exercises/grupo/{grupo}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"\n🎯 Ejercicios de {grupo}:")
    print(f"Status: {response.status_code}")
    exercises = response.json()
    
    for exercise in exercises:
        print(f"  - {exercise['nombre']}")

def create_routine(token, exercises):
    """Ejemplo: Crear rutina"""
    url = f"{BASE_URL}/routines/"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Usar los primeros 3 ejercicios para la rutina
    series = []
    for i, exercise in enumerate(exercises[:3]):
        series.append({
            "ejercicio_id": exercise["id"],
            "orden": i + 1,
            "series": 3,
            "repeticiones_min": 8,
            "repeticiones_max": 12,
            "tiempo_descanso": 90
        })
    
    data = {
        "nombre": "Mi Primera Rutina",
        "descripcion": "Rutina de ejemplo creada via API",
        "categoria": "hipertrofia",
        "duracion_estimada": 45,
        "nivel_dificultad": "principiante",
        "is_public": False,
        "series": series
    }
    
    response = requests.post(url, json=data, headers=headers)
    print("\n📋 Crear rutina:")
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        rutina = response.json()
        print(f"Rutina creada: {rutina['nombre']}")
        print(f"Ejercicios en la rutina: {len(rutina['series'])}")
        return rutina
    else:
        print(f"Error: {response.json()}")
    return None

def get_my_routines(token):
    """Ejemplo: Obtener mis rutinas"""
    url = f"{BASE_URL}/routines/mis-rutinas"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print("\n📚 Mis rutinas:")
    print(f"Status: {response.status_code}")
    routines = response.json()
    
    for routine in routines:
        print(f"  - {routine['nombre']} ({routine['categoria']})")

def add_favorite_exercise(token, exercise_id):
    """Ejemplo: Agregar ejercicio a favoritos"""
    url = f"{BASE_URL}/exercises/favoritos/{exercise_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(url, headers=headers)
    print(f"\n⭐ Agregar ejercicio {exercise_id} a favoritos:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    """Función principal de ejemplos"""
    print("🏋️ Ejemplos de uso de Gainz API\n")
    
    try:
        # 1. Registrar usuario
        register_user()
        
        # 2. Login
        token = login_user()
        if not token:
            print("❌ Error en login, no se puede continuar")
            return
        
        # 3. Obtener ejercicios
        exercises = get_exercises(token)
        
        # 4. Obtener ejercicios por grupo
        get_exercises_by_group(token, "pectorales")
        
        # 5. Crear rutina
        create_routine(token, exercises)
        
        # 6. Ver mis rutinas
        get_my_routines(token)
        
        # 7. Agregar ejercicio a favoritos
        if exercises:
            add_favorite_exercise(token, exercises[0]["id"])
        
        print("\n✅ Ejemplos completados exitosamente!")
        print("🌐 Visita http://localhost:8000/docs para más información")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API.")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()