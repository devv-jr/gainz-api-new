"""
Script para poblar la base de datos con ejercicios e imágenes
"""
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Exercise, Rutina, SerieEjercicio, User
from auth import get_password_hash

# Datos de ejercicios organizados por grupo muscular
EXERCISES_DATA = {
    "abs": [
        {
            "nombre": "Abdominales Brazos Estirados",
            "descripcion": "Ejercicio para fortalecer los músculos abdominales con brazos estirados",
            "instrucciones": "Acuéstate boca arriba, extiende los brazos hacia arriba y realiza el movimiento abdominal",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "core, estabilizadores",
            "imagen": "abdominales-brazos-estirados.png"
        },
        {
            "nombre": "Abdominales Cuerda Polea Alta",
            "descripcion": "Abdominales usando cuerda en polea alta para mayor resistencia",
            "instrucciones": "Arrodíllate frente a la polea alta, sujeta la cuerda y lleva los codos hacia las rodillas",
            "nivel_dificultad": "avanzado",
            "equipo_necesario": "Polea alta, cuerda",
            "musculos_secundarios": "oblicuos",
            "imagen": "abdominales-cuerda-polea-alta.png"
        },
        {
            "nombre": "Abdominales Máquina",
            "descripcion": "Ejercicio de abdominales en máquina específica",
            "instrucciones": "Siéntate en la máquina, ajusta el peso y realiza el movimiento de flexión abdominal",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Máquina de abdominales",
            "musculos_secundarios": "core",
            "imagen": "abdominales-maquina.png"
        },
        {
            "nombre": "Crunch Oblicuo",
            "descripcion": "Variación de crunch para trabajar músculos oblicuos",
            "instrucciones": "Acuéstate de lado y realiza crunches llevando el codo hacia la rodilla del mismo lado",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "core, oblicuos",
            "imagen": "crunch-oblicuo.png"
        },
        {
            "nombre": "Crunch",
            "descripcion": "Ejercicio básico de abdominales",
            "instrucciones": "Acuéstate boca arriba, manos detrás de la cabeza, eleva el torso hacia las rodillas",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "core",
            "imagen": "crunch.png"
        },
        {
            "nombre": "Elevación de Piernas",
            "descripcion": "Ejercicio para el abdomen inferior elevando las piernas",
            "instrucciones": "Acuéstate boca arriba y eleva las piernas manteniendo las rodillas rectas",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "hip flexors",
            "imagen": "elevacion-de-piernas.png"
        },
        {
            "nombre": "Encogimientos de Rodillas",
            "descripcion": "Ejercicio llevando las rodillas hacia el pecho",
            "instrucciones": "Sentado, lleva las rodillas hacia el pecho manteniendo el equilibrio",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "core, hip flexors",
            "imagen": "encogimientos-de-rodillas.png"
        },
        {
            "nombre": "Plancha con Flexión",
            "descripcion": "Combinación de plancha con push-up",
            "instrucciones": "Mantén posición de plancha y realiza flexiones de brazos",
            "nivel_dificultad": "avanzado",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "pecho, hombros, tríceps",
            "imagen": "plancha-con-flexion.png"
        },
        {
            "nombre": "Plancha",
            "descripcion": "Ejercicio isométrico para fortalecer el core",
            "instrucciones": "Mantén posición de plancha con cuerpo recto desde cabeza hasta talones",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "hombros, glúteos",
            "imagen": "plancha.png"
        }
    ],
    "biceps": [
        {
            "nombre": "Curl Alterno Mancuernas",
            "descripcion": "Curl de bíceps alternando brazos con mancuernas",
            "instrucciones": "De pie, alterna el curl de cada brazo manteniendo los codos fijos",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Mancuernas",
            "musculos_secundarios": "antebrazo",
            "imagen": "curl-alterno-mancuernas.png"
        },
        {
            "nombre": "Curl Alterno Martillo Mancuernas",
            "descripcion": "Curl estilo martillo alternando brazos",
            "instrucciones": "Curl con agarre neutro alternando brazos",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Mancuernas",
            "musculos_secundarios": "antebrazo, braquiorradial",
            "imagen": "curl-alterno-martillo-mancuernas.png"
        },
        {
            "nombre": "Curl Barra Invertido",
            "descripcion": "Curl de bíceps con agarre prono (invertido)",
            "instrucciones": "Curl con barra usando agarre overhand",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Barra",
            "musculos_secundarios": "antebrazo, braquiorradial",
            "imagen": "curl-barra-invertido.png"
        },
        {
            "nombre": "Curl con Barra Z",
            "descripcion": "Curl de bíceps usando barra Z o EZ",
            "instrucciones": "Curl manteniendo los codos fijos a los costados",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Barra Z",
            "musculos_secundarios": "antebrazo",
            "imagen": "curl-con-barra-z.png"
        },
        {
            "nombre": "Curl con Barra",
            "descripcion": "Curl básico de bíceps con barra recta",
            "instrucciones": "De pie, curl con barra manteniendo postura recta",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Barra",
            "musculos_secundarios": "antebrazo",
            "imagen": "curl-con-barra.png"
        }
    ],
    "espalda": [
        {
            "nombre": "Dominadas Agarre Supinado",
            "descripcion": "Dominadas con palmas hacia ti",
            "instrucciones": "Cuelga de la barra con agarre supinado y elévate hasta que la barbilla pase la barra",
            "nivel_dificultad": "avanzado",
            "equipo_necesario": "Barra de dominadas",
            "musculos_secundarios": "bíceps",
            "imagen": "dominadas-agarre-supinado.png"
        },
        {
            "nombre": "Dominadas",
            "descripcion": "Dominadas tradicionales con agarre pronado",
            "instrucciones": "Cuelga de la barra y elévate hasta que la barbilla pase la barra",
            "nivel_dificultad": "avanzado",
            "equipo_necesario": "Barra de dominadas",
            "musculos_secundarios": "bíceps, core",
            "imagen": "dominadas.png"
        },
        {
            "nombre": "Peso Muerto",
            "descripcion": "Ejercicio compuesto fundamental para espalda y piernas",
            "instrucciones": "Levanta la barra desde el suelo manteniendo la espalda recta",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Barra, discos",
            "musculos_secundarios": "glúteos, cuádriceps, trapecio",
            "imagen": "peso-muerto.png"
        },
        {
            "nombre": "Remo con Barra",
            "descripcion": "Remo inclinado con barra",
            "instrucciones": "Inclínate hacia adelante y rema la barra hacia el abdomen",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Barra, discos",
            "musculos_secundarios": "bíceps, deltoides posterior",
            "imagen": "remo-con-barra.png"
        },
        {
            "nombre": "Jalón al Pecho Agarre Ancho",
            "descripcion": "Jalón en polea alta con agarre amplio",
            "instrucciones": "Tira de la barra hacia el pecho con agarre amplio",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Polea alta",
            "musculos_secundarios": "bíceps, deltoides posterior",
            "imagen": "jalon-al-pecho-agarre-ancho.png"
        }
    ],
    "gemelos": [
        {
            "nombre": "Elevación de Gemelos de Pie",
            "descripcion": "Elevación de talones de pie para desarrollar gemelos",
            "instrucciones": "De pie, eleva los talones lo más alto posible y baja lentamente",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Ninguno o mancuernas",
            "musculos_secundarios": "sóleo",
            "imagen": "elevacion-de-gemelos-de-pie.png"
        },
        {
            "nombre": "Elevación de Gemelos Sentado",
            "descripcion": "Elevación de gemelos en posición sentada",
            "instrucciones": "Sentado, coloca peso sobre las rodillas y eleva los talones",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Banco, peso",
            "musculos_secundarios": "sóleo",
            "imagen": "elevacion-de-gemelos-sentado.png"
        }
    ],
    "hombros": [
        {
            "nombre": "Press Militar de Pie",
            "descripcion": "Press de hombros de pie con barra",
            "instrucciones": "De pie, presiona la barra desde los hombros hacia arriba",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Barra, discos",
            "musculos_secundarios": "tríceps, core",
            "imagen": "press-militar-de-pie.png"
        },
        {
            "nombre": "Press de Hombro Mancuernas",
            "descripcion": "Press de hombros con mancuernas",
            "instrucciones": "Sentado o de pie, presiona las mancuernas desde los hombros hacia arriba",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Mancuernas",
            "musculos_secundarios": "tríceps",
            "imagen": "press-de-hombro-mancuernas.png"
        },
        {
            "nombre": "Elevaciones Laterales",
            "descripcion": "Elevaciones laterales para deltoides medio",
            "instrucciones": "Con mancuernas, eleva los brazos lateralmente hasta la altura de los hombros",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Mancuernas",
            "musculos_secundarios": "trapecio",
            "imagen": "elevaciones-laterales.png"
        },
        {
            "nombre": "Elevaciones Frontales",
            "descripcion": "Elevaciones frontales para deltoides anterior",
            "instrucciones": "Eleva las mancuernas al frente hasta la altura de los hombros",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Mancuernas",
            "musculos_secundarios": "core",
            "imagen": "elevaciones-frontales.png"
        }
    ],
    "pectorales": [
        {
            "nombre": "Press Banca",
            "descripcion": "Ejercicio fundamental para el desarrollo del pecho",
            "instrucciones": "Acostado en banco, baja la barra al pecho y presiona hacia arriba",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Banco, barra, discos",
            "musculos_secundarios": "tríceps, deltoides anterior",
            "imagen": "press-banca.png"
        },
        {
            "nombre": "Press Banca Inclinado",
            "descripcion": "Press de banca en banco inclinado",
            "instrucciones": "En banco inclinado, presiona la barra desde el pecho superior",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Banco inclinado, barra, discos",
            "musculos_secundarios": "tríceps, deltoides anterior",
            "imagen": "press-banca-inclinado.png"
        },
        {
            "nombre": "Press Banca Mancuernas",
            "descripcion": "Press de pecho con mancuernas",
            "instrucciones": "Acostado, presiona las mancuernas desde el pecho hacia arriba",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Banco, mancuernas",
            "musculos_secundarios": "tríceps, deltoides anterior",
            "imagen": "press-banca-mancuernas.png"
        },
        {
            "nombre": "Flexiones",
            "descripcion": "Flexiones de pecho tradicionales",
            "instrucciones": "En posición de plancha, baja el pecho al suelo y presiona hacia arriba",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Ninguno",
            "musculos_secundarios": "tríceps, core",
            "imagen": "flexiones.png"
        },
        {
            "nombre": "Aperturas Mancuernas",
            "descripcion": "Aperturas para pecho con mancuernas",
            "instrucciones": "Acostado, abre los brazos lateralmente y junta las mancuernas sobre el pecho",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Banco, mancuernas",
            "musculos_secundarios": "deltoides anterior",
            "imagen": "aperturas-mancuernas.png"
        }
    ],
    "piernas": [
        {
            "nombre": "Sentadilla",
            "descripcion": "Ejercicio fundamental para desarrollo de piernas",
            "instrucciones": "Baja como si fueras a sentarte manteniendo la espalda recta",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Ninguno o barra",
            "musculos_secundarios": "glúteos, core",
            "imagen": "sentadilla.png"
        },
        {
            "nombre": "Sentadilla Frontal",
            "descripcion": "Sentadilla con barra en posición frontal",
            "instrucciones": "Sentadilla con la barra apoyada en la parte frontal de los hombros",
            "nivel_dificultad": "avanzado",
            "equipo_necesario": "Barra, discos",
            "musculos_secundarios": "glúteos, core",
            "imagen": "sentadilla-frontal.png"
        },
        {
            "nombre": "Peso Muerto Rumano Barra",
            "descripcion": "Peso muerto rumano enfocado en isquiotibiales",
            "instrucciones": "Baja la barra manteniendo las piernas semi-flexionadas",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Barra, discos",
            "musculos_secundarios": "glúteos, espalda baja",
            "imagen": "peso-muerto-rumano-barra.png"
        },
        {
            "nombre": "Prensa",
            "descripcion": "Prensa de piernas en máquina",
            "instrucciones": "En la máquina de prensa, presiona el peso con las piernas",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Máquina de prensa",
            "musculos_secundarios": "glúteos",
            "imagen": "prensa.png"
        },
        {
            "nombre": "Zancada",
            "descripcion": "Zancadas para trabajar piernas unilateralmente",
            "instrucciones": "Da un paso largo hacia adelante y baja la rodilla trasera",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Ninguno o mancuernas",
            "musculos_secundarios": "glúteos, core",
            "imagen": "zancada.png"
        }
    ],
    "triceps": [
        {
            "nombre": "Extensión Tríceps Polea",
            "descripcion": "Extensión de tríceps en polea alta",
            "instrucciones": "Con cuerda o barra, extiende los brazos hacia abajo manteniendo codos fijos",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Polea alta",
            "musculos_secundarios": "antebrazo",
            "imagen": "extension-triceps-polea.png"
        },
        {
            "nombre": "Fondos Banco",
            "descripcion": "Fondos de tríceps usando un banco",
            "instrucciones": "Apoya las manos en el banco detrás de ti y baja el cuerpo",
            "nivel_dificultad": "principiante",
            "equipo_necesario": "Banco",
            "musculos_secundarios": "pecho, hombros",
            "imagen": "fondos-banco.png"
        },
        {
            "nombre": "Fondos Barras Paralelas",
            "descripcion": "Fondos en barras paralelas",
            "instrucciones": "Suspéndete entre barras paralelas y baja/sube el cuerpo",
            "nivel_dificultad": "avanzado",
            "equipo_necesario": "Barras paralelas",
            "musculos_secundarios": "pecho, hombros",
            "imagen": "fondos-barras-paralelas.png"
        },
        {
            "nombre": "Press Banca Cerrado",
            "descripcion": "Press de banca con agarre cerrado para tríceps",
            "instrucciones": "Press de banca con las manos juntas",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Banco, barra",
            "musculos_secundarios": "pecho",
            "imagen": "press-banca-cerrado.png"
        },
        {
            "nombre": "Extensión Tríceps Tumbado",
            "descripcion": "Extensiones de tríceps acostado",
            "instrucciones": "Acostado, extiende los brazos hacia arriba desde la frente",
            "nivel_dificultad": "intermedio",
            "equipo_necesario": "Banco, barra o mancuernas",
            "musculos_secundarios": "antebrazo",
            "imagen": "extension-triceps-tumbado.png"
        }
    ]
}

def create_exercises(db: Session):
    """Crear ejercicios en la base de datos"""
    print("🏋️ Creando ejercicios...")
    
    for grupo_muscular, exercises in EXERCISES_DATA.items():
        print(f"  📂 Procesando grupo muscular: {grupo_muscular}")
        
        for exercise_data in exercises:
            # Verificar si el ejercicio ya existe
            existing_exercise = db.query(Exercise).filter(
                Exercise.nombre == exercise_data["nombre"]
            ).first()
            
            if existing_exercise:
                print(f"    ⚠️  Ejercicio '{exercise_data['nombre']}' ya existe, omitiendo...")
                continue
            
            # Crear ejercicio
            exercise = Exercise(
                nombre=exercise_data["nombre"],
                grupo_muscular=grupo_muscular,
                descripcion=exercise_data["descripcion"],
                instrucciones=exercise_data["instrucciones"],
                nivel_dificultad=exercise_data["nivel_dificultad"],
                equipo_necesario=exercise_data["equipo_necesario"],
                musculos_secundarios=exercise_data["musculos_secundarios"],
                imagen_url=f"/images/{grupo_muscular}/{exercise_data['imagen']}"
            )
            
            db.add(exercise)
            print(f"    ✅ Creado: {exercise_data['nombre']}")
    
    db.commit()
    print("✅ Ejercicios creados exitosamente!")

def create_sample_routines(db: Session):
    """Crear rutinas de ejemplo"""
    print("📋 Creando rutinas de ejemplo...")
    
    # Crear usuario admin para las plantillas
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            email="admin@gainzapi.com",
            username="admin",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    
    # Rutina Push (Empuje)
    push_routine = Rutina(
        nombre="Rutina Push - Pecho, Hombros, Tríceps",
        descripcion="Rutina de entrenamiento enfocada en músculos de empuje",
        categoria="hipertrofia",
        duracion_estimada=60,
        nivel_dificultad="intermedio",
        is_public=True,
        is_template=True,
        owner_id=admin_user.id
    )
    db.add(push_routine)
    db.commit()
    db.refresh(push_routine)
    
    # Ejercicios para rutina Push
    push_exercises = [
        {"nombre": "Press Banca", "series": 4, "rep_min": 8, "rep_max": 10, "orden": 1},
        {"nombre": "Press Banca Inclinado", "series": 3, "rep_min": 10, "rep_max": 12, "orden": 2},
        {"nombre": "Press de Hombro Mancuernas", "series": 3, "rep_min": 10, "rep_max": 12, "orden": 3},
        {"nombre": "Elevaciones Laterales", "series": 3, "rep_min": 12, "rep_max": 15, "orden": 4},
        {"nombre": "Fondos Banco", "series": 3, "rep_min": 12, "rep_max": 15, "orden": 5},
        {"nombre": "Extensión Tríceps Polea", "series": 3, "rep_min": 12, "rep_max": 15, "orden": 6},
    ]
    
    for ex_data in push_exercises:
        exercise = db.query(Exercise).filter(Exercise.nombre == ex_data["nombre"]).first()
        if exercise:
            serie = SerieEjercicio(
                rutina_id=push_routine.id,
                ejercicio_id=exercise.id,
                orden=ex_data["orden"],
                series=ex_data["series"],
                repeticiones_min=ex_data["rep_min"],
                repeticiones_max=ex_data["rep_max"],
                tiempo_descanso=90
            )
            db.add(serie)
    
    # Rutina Pull (Tirón)
    pull_routine = Rutina(
        nombre="Rutina Pull - Espalda, Bíceps",
        descripcion="Rutina de entrenamiento enfocada en músculos de tirón",
        categoria="hipertrofia",
        duracion_estimada=60,
        nivel_dificultad="intermedio",
        is_public=True,
        is_template=True,
        owner_id=admin_user.id
    )
    db.add(pull_routine)
    db.commit()
    db.refresh(pull_routine)
    
    # Ejercicios para rutina Pull
    pull_exercises = [
        {"nombre": "Dominadas", "series": 4, "rep_min": 6, "rep_max": 10, "orden": 1},
        {"nombre": "Remo con Barra", "series": 4, "rep_min": 8, "rep_max": 10, "orden": 2},
        {"nombre": "Jalón al Pecho Agarre Ancho", "series": 3, "rep_min": 10, "rep_max": 12, "orden": 3},
        {"nombre": "Curl con Barra", "series": 3, "rep_min": 10, "rep_max": 12, "orden": 4},
        {"nombre": "Curl Alterno Mancuernas", "series": 3, "rep_min": 12, "rep_max": 15, "orden": 5},
    ]
    
    for ex_data in pull_exercises:
        exercise = db.query(Exercise).filter(Exercise.nombre == ex_data["nombre"]).first()
        if exercise:
            serie = SerieEjercicio(
                rutina_id=pull_routine.id,
                ejercicio_id=exercise.id,
                orden=ex_data["orden"],
                series=ex_data["series"],
                repeticiones_min=ex_data["rep_min"],
                repeticiones_max=ex_data["rep_max"],
                tiempo_descanso=90
            )
            db.add(serie)
    
    # Rutina Legs (Piernas)
    legs_routine = Rutina(
        nombre="Rutina Legs - Piernas y Glúteos",
        descripcion="Rutina completa para el tren inferior",
        categoria="hipertrofia",
        duracion_estimada=75,
        nivel_dificultad="intermedio",
        is_public=True,
        is_template=True,
        owner_id=admin_user.id
    )
    db.add(legs_routine)
    db.commit()
    db.refresh(legs_routine)
    
    # Ejercicios para rutina Legs
    legs_exercises = [
        {"nombre": "Sentadilla", "series": 4, "rep_min": 8, "rep_max": 12, "orden": 1},
        {"nombre": "Peso Muerto Rumano Barra", "series": 4, "rep_min": 8, "rep_max": 10, "orden": 2},
        {"nombre": "Prensa", "series": 3, "rep_min": 12, "rep_max": 15, "orden": 3},
        {"nombre": "Zancada", "series": 3, "rep_min": 12, "rep_max": 15, "orden": 4},
        {"nombre": "Elevación de Gemelos de Pie", "series": 4, "rep_min": 15, "rep_max": 20, "orden": 5},
    ]
    
    for ex_data in legs_exercises:
        exercise = db.query(Exercise).filter(Exercise.nombre == ex_data["nombre"]).first()
        if exercise:
            serie = SerieEjercicio(
                rutina_id=legs_routine.id,
                ejercicio_id=exercise.id,
                orden=ex_data["orden"],
                series=ex_data["series"],
                repeticiones_min=ex_data["rep_min"],
                repeticiones_max=ex_data["rep_max"],
                tiempo_descanso=120
            )
            db.add(serie)
    
    db.commit()
    print("✅ Rutinas de ejemplo creadas exitosamente!")

def main():
    """Función principal para poblar la base de datos"""
    print("🚀 Iniciando población de la base de datos...")
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # Crear ejercicios
        create_exercises(db)
        
        # Crear rutinas de ejemplo
        create_sample_routines(db)
        
        # Estadísticas finales
        total_exercises = db.query(Exercise).count()
        total_routines = db.query(Rutina).count()
        
        print(f"\n📊 Estadísticas finales:")
        print(f"   💪 Ejercicios totales: {total_exercises}")
        print(f"   📋 Rutinas totales: {total_routines}")
        print(f"\n🎉 ¡Base de datos poblada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()