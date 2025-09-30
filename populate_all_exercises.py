"""
Script para crear TODOS los ejercicios basados en las imágenes reales
"""
import os
from pathlib import Path
from database import SessionLocal, engine
from models import Base, Exercise, Rutina, SerieEjercicio, User
from auth import get_password_hash

def clean_exercise_name(filename):
    """Limpiar nombre del archivo para crear nombre del ejercicio"""
    # Remover extensión
    name = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
    # Reemplazar guiones con espacios
    name = name.replace('-', ' ')
    # Capitalizar cada palabra
    return name.title()

def get_exercise_info(name, grupo_muscular):
    """Obtener información detallada del ejercicio basado en el nombre y grupo"""
    
    # Mapeo de descripciones específicas por ejercicio
    descriptions = {
        # Abdominales
        "abdominales brazos estirados": "Ejercicio de abdominales manteniendo los brazos extendidos por encima de la cabeza.",
        "abdominales cuerda polea alta": "Abdominales en polea alta usando cuerda para mayor resistencia.",
        "abdominales maquina": "Ejercicio de abdominales en máquina específica con resistencia ajustable.",
        "crunch oblicuo": "Variación de crunch para trabajar específicamente los músculos oblicuos.",
        "crunch": "Ejercicio básico y fundamental para fortalecer los músculos abdominales.",
        "elevacion de piernas": "Ejercicio para trabajar la parte inferior del abdomen elevando las piernas.",
        "encogimientos de rodillas": "Ejercicio llevando las rodillas hacia el pecho para trabajar el core.",
        "plancha con flexion": "Combinación de plancha isométrica con flexiones de brazos.",
        "plancha": "Ejercicio isométrico fundamental para fortalecer todo el core.",
        
        # Bíceps
        "curl alterno mancuernas": "Curl de bíceps alternando brazos con mancuernas.",
        "curl alterno martillo mancuernas": "Curl estilo martillo alternando brazos con agarre neutro.",
        "curl barra invertido": "Curl de bíceps con agarre prono para trabajar braquiorradial.",
        "curl con barra z": "Curl de bíceps usando barra Z para mayor comodidad en las muñecas.",
        "curl con barra": "Curl básico de bíceps con barra recta.",
        "curl con cuerda polea": "Curl de bíceps en polea usando cuerda.",
        "curl concentrado mancuernas": "Curl concentrado sentado para aislamiento máximo del bíceps.",
        "curl de cable con barra recta polea baja": "Curl de bíceps en polea baja con barra recta.",
        "curl de cable en polea baja una mano": "Curl unilateral en polea baja para trabajar cada brazo por separado.",
        "curl de cable polea alta de pie": "Curl de bíceps en polea alta de pie.",
        "curl inclinado mancuernas": "Curl de bíceps en banco inclinado para mayor estiramiento.",
        "curl muñeca con barra sentado": "Ejercicio para fortalecer músculos del antebrazo.",
        "curl predicador con barra z": "Curl en banco predicador con barra Z.",
        "extension de muñeca barra sentado": "Ejercicio para extensores del antebrazo.",
        
        # Espalda
        "dominadas agarre supinado": "Dominadas con palmas hacia el cuerpo, trabaja más los bíceps.",
        "dominadas": "Dominadas clásicas con agarre prono, excelente para dorsales.",
        "encogimiento de hombros barra": "Encogimientos de hombros con barra para trapecio.",
        "encogimiento de hombros mancuernas": "Encogimientos de hombros con mancuernas.",
        "jalon al pecho agarre ancho": "Jalón en polea alta con agarre amplio para dorsales.",
        "jalon al pecho agarre cerrado": "Jalón con agarre cerrado para mayor activación de bíceps.",
        "jalon al pecho agarre invertido": "Jalón con agarre supinado.",
        "jalon dorsal con brazos rectos": "Jalón con brazos rectos para dorsales inferiores.",
        "jalon polea con cuerda": "Jalón en polea usando cuerda.",
        "peso muerto con barra hexagonal": "Peso muerto usando barra hexagonal o trap bar.",
        "peso muerto con mancuernas": "Peso muerto utilizando mancuernas.",
        "peso muerto sumo": "Variante de peso muerto con stance amplio.",
        "peso muerto": "Ejercicio compuesto fundamental para toda la cadena posterior.",
        "pullover con barra": "Pullover con barra para dorsales y expansión de caja torácica.",
        "pullover con mancuerna": "Pullover con mancuerna, excelente para dorsales.",
        "remo con barra agarre supinado": "Remo con barra usando agarre supinado.",
        "remo con barra": "Remo inclinado con barra, fundamental para espalda media.",
        "remo con mancuerna una mano": "Remo unilateral con mancuerna.",
        "remo en barra t": "Remo en barra T para espalda media y posterior.",
        "remo inclinado con mancuernas": "Remo inclinado usando mancuernas.",
        "remo maquina": "Remo en máquina para espalda.",
        
        # Gemelos
        "elevacion de gemelos de pie": "Elevación de talones de pie para desarrollar gemelos.",
        "elevacion de gemelos sentado": "Elevación de gemelos en posición sentada.",
        
        # Hombros
        "cruces inversos polea alta": "Cruces inversos en polea alta para deltoides posterior.",
        "elevaciones frontales agarre neutro": "Elevaciones frontales con agarre neutro.",
        "elevaciones frontales barra": "Elevaciones frontales usando barra.",
        "elevaciones frontales cable a una mano": "Elevaciones frontales unilaterales en cable.",
        "elevaciones frontales polea baja neutro": "Elevaciones frontales en polea baja con agarre neutro.",
        "elevaciones frontales": "Elevaciones frontales básicas con mancuernas.",
        "elevaciones laterales cable bajo": "Elevaciones laterales en polea baja.",
        "elevaciones laterales": "Elevaciones laterales básicas para deltoides medio.",
        "elevaciones posteriores pajaro": "Ejercicio pájaro para deltoides posterior.",
        "press de hombro mancuernas": "Press de hombros con mancuernas.",
        "press de hombros en maquina smith": "Press de hombros en máquina Smith.",
        "press militar con barra sentado": "Press militar sentado con barra.",
        "press militar de pie": "Press militar de pie con barra.",
        "press militar mancuernas": "Press militar con mancuernas.",
        "press militar tras nuca": "Press militar tras nuca (requiere flexibilidad).",
        "press militar": "Press militar básico con barra.",
        "remo alto barra": "Remo alto con barra para deltoides y trapecio.",
        
        # Pectorales
        "aperturas mancuernas inclinado": "Aperturas en banco inclinado con mancuernas.",
        "aperturas mancuernas": "Aperturas en banco plano con mancuernas.",
        "cruce poleas": "Cruces en poleas para pectorales.",
        "flexiones": "Flexiones de pecho clásicas.",
        "peck deck": "Ejercicio en máquina pec deck para pectorales.",
        "press banca inclinado": "Press de banca en banco inclinado.",
        "press banca mancuernas": "Press de banca con mancuernas.",
        "press banca": "Press de banca básico con barra.",
        "press declinado barra": "Press de banca declinado con barra.",
        "press declinado mancuernas": "Press declinado con mancuernas.",
        "press inclinado mancuernas": "Press inclinado con mancuernas.",
        "press maquina sentado": "Press de pecho en máquina.",
        
        # Piernas
        "burpees": "Ejercicio completo de cuerpo que incluye sentadilla y salto.",
        "caminata de pato": "Ejercicio de movilidad y fuerza en posición de sentadilla.",
        "contragolpe con cable": "Ejercicio para glúteos usando cable.",
        "curl de femoral": "Curl de isquiotibiales en máquina.",
        "curl de piernas sentado": "Curl de isquiotibiales sentado.",
        "ejercicio superman cuadrupedia": "Ejercicio Superman en cuadrupedia para core y glúteos.",
        "elevaciones de caderas con barra": "Hip thrust con barra para glúteos.",
        "elevaciones de caderas en smith": "Hip thrust en máquina Smith.",
        "elevaciones de rodilla": "Elevaciones de rodilla para core y hip flexors.",
        "extension a una pierna": "Extensión unilateral de cuádriceps.",
        "extension de piernas": "Extensión de cuádriceps en máquina.",
        "peso muerto rumano barra": "Peso muerto rumano con barra para isquiotibiales.",
        "peso muerto rumano mancuernas": "Peso muerto rumano con mancuernas.",
        "prensa": "Prensa de piernas en máquina.",
        "puente con peso corporal": "Puente de glúteos con peso corporal.",
        "puentes a una pierna": "Puentes unilaterales de glúteos.",
        "salto rodillas al pecho": "Ejercicio pliométrico de salto.",
        "sentadilla bulgara barra": "Sentadilla búlgara con barra.",
        "sentadilla bulgara": "Sentadilla búlgara unilateral.",
        "sentadilla con mini banda": "Sentadilla con banda elástica.",
        "sentadilla con salto": "Sentadilla pliométrica con salto.",
        "sentadilla frontal": "Sentadilla frontal con barra.",
        "sentadilla goblet mancuerna": "Sentadilla goblet con mancuerna.",
        "sentadilla hack": "Sentadilla hack en máquina.",
        "sentadilla sobre la pared": "Sentadilla isométrica contra la pared.",
        "sentadilla": "Sentadilla básica con peso corporal o barra.",
        "sentadillas con balon": "Sentadilla usando balón de ejercicio.",
        "sentadillas peso corporal": "Sentadillas básicas sin peso adicional.",
        "zancada": "Zancadas para trabajar piernas unilateralmente.",
        
        # Tríceps
        "extension triceps agarre inverso barra": "Extensión de tríceps con agarre inverso.",
        "extension triceps cable una mano supinado": "Extensión unilateral con agarre supinado.",
        "extension triceps cable una mano": "Extensión de tríceps unilateral en cable.",
        "extension triceps cuerda": "Extensión de tríceps con cuerda en polea.",
        "extension triceps mancuernas sentado": "Extensión de tríceps sentado con mancuernas.",
        "extension triceps mancuernas tumbado": "Extensión de tríceps acostado con mancuernas.",
        "extension triceps polea": "Extensión de tríceps en polea alta.",
        "extension triceps tumbado": "Extensión de tríceps acostado con barra.",
        "fondos banco": "Fondos de tríceps usando banco.",
        "fondos barras paralelas": "Fondos en barras paralelas.",
        "patadas traseras": "Patadas traseras de tríceps con mancuernas.",
        "press banca cerrado": "Press de banca con agarre cerrado para tríceps.",
        "press frances sentado barra": "Press francés sentado con barra.",
    }
    
    # Obtener descripción específica o genérica
    description = descriptions.get(name.lower(), f"Ejercicio efectivo para el desarrollo de {grupo_muscular}.")
    
    # Determinar equipo necesario
    equipment = "Peso corporal"
    if any(word in name.lower() for word in ["barra", "press", "peso muerto"]):
        equipment = "Barra y discos"
    elif any(word in name.lower() for word in ["mancuernas", "mancuerna"]):
        equipment = "Mancuernas"
    elif any(word in name.lower() for word in ["polea", "cable", "jalon"]):
        equipment = "Polea/Cable"
    elif any(word in name.lower() for word in ["maquina", "smith", "peck deck", "prensa"]):
        equipment = "Máquina"
    elif any(word in name.lower() for word in ["cuerda"]):
        equipment = "Cuerda y polea"
    elif any(word in name.lower() for word in ["banda", "mini banda"]):
        equipment = "Banda elástica"
    elif any(word in name.lower() for word in ["banco"]):
        equipment = "Banco"
    
    # Determinar nivel de dificultad
    difficulty = "intermedio"
    if any(word in name.lower() for word in ["peso corporal", "flexiones", "plancha", "sentadilla", "crunch"]):
        difficulty = "principiante"
    elif any(word in name.lower() for word in ["dominadas", "peso muerto", "frontal", "bulgara", "concentrado"]):
        difficulty = "avanzado"
    
    # Determinar músculos secundarios
    secondary_muscles = ""
    if grupo_muscular == "abs":
        secondary_muscles = "core, estabilizadores"
    elif grupo_muscular == "biceps":
        secondary_muscles = "antebrazo"
    elif grupo_muscular == "espalda":
        secondary_muscles = "bíceps, deltoides posterior"
    elif grupo_muscular == "gemelos":
        secondary_muscles = "sóleo"
    elif grupo_muscular == "hombros":
        secondary_muscles = "tríceps, trapecio"
    elif grupo_muscular == "pectorales":
        secondary_muscles = "tríceps, deltoides anterior"
    elif grupo_muscular == "piernas":
        secondary_muscles = "glúteos, core"
    elif grupo_muscular == "triceps":
        secondary_muscles = "antebrazo"
    
    return {
        "descripcion": description,
        "instrucciones": f"Ejecuta {name.lower()} manteniendo una técnica correcta y controlada.",
        "equipo_necesario": equipment,
        "nivel_dificultad": difficulty,
        "musculos_secundarios": secondary_muscles
    }

def populate_all_exercises():
    """Poblar la base de datos con TODOS los ejercicios de las imágenes"""
    db = SessionLocal()
    
    try:
        # Crear tablas si no existen
        Base.metadata.create_all(bind=engine)
        
        images_dir = Path("images")
        if not images_dir.exists():
            print("❌ Directorio 'images' no encontrado")
            return
        
        exercise_count = 0
        total_images = 0
        
        print("🔍 Analizando todas las imágenes...")
        
        # Contar total de imágenes primero
        for grupo_dir in images_dir.iterdir():
            if grupo_dir.is_dir() and grupo_dir.name != ".gitkeep":
                for image_file in grupo_dir.iterdir():
                    if image_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                        total_images += 1
        
        print(f"📊 Total de imágenes encontradas: {total_images}")
        print("\n🏋️ Creando ejercicios...")
        
        # Recorrer cada grupo muscular
        for grupo_dir in sorted(images_dir.iterdir()):
            if grupo_dir.is_dir() and grupo_dir.name != ".gitkeep":
                grupo_muscular = grupo_dir.name
                print(f"\n📁 Procesando grupo: {grupo_muscular.upper()}")
                
                # Recorrer imágenes en el grupo
                for image_file in sorted(grupo_dir.iterdir()):
                    if image_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                        # Crear nombre del ejercicio
                        exercise_name = clean_exercise_name(image_file.name)
                        
                        # Verificar si el ejercicio ya existe
                        existing = db.query(Exercise).filter(
                            Exercise.nombre == exercise_name,
                            Exercise.grupo_muscular == grupo_muscular
                        ).first()
                        
                        if existing:
                            print(f"  ⏭️  {exercise_name} (ya existe)")
                            continue
                        
                        # Obtener información del ejercicio
                        exercise_info = get_exercise_info(exercise_name, grupo_muscular)
                        
                        # Crear ejercicio
                        exercise = Exercise(
                            nombre=exercise_name,
                            grupo_muscular=grupo_muscular,
                            descripcion=exercise_info["descripcion"],
                            instrucciones=exercise_info["instrucciones"],
                            nivel_dificultad=exercise_info["nivel_dificultad"],
                            equipo_necesario=exercise_info["equipo_necesario"],
                            musculos_secundarios=exercise_info["musculos_secundarios"],
                            imagen_url=f"/images/{grupo_muscular}/{image_file.name}"
                        )
                        
                        db.add(exercise)
                        exercise_count += 1
                        print(f"  ✅ {exercise_name}")
        
        # Guardar cambios
        db.commit()
        
        # Estadísticas finales
        total_exercises = db.query(Exercise).count()
        exercises_by_group = {}
        
        for grupo in ["abs", "biceps", "espalda", "gemelos", "hombros", "pectorales", "piernas", "triceps"]:
            count = db.query(Exercise).filter(Exercise.grupo_muscular == grupo).count()
            exercises_by_group[grupo] = count
        
        print(f"\n🎉 ¡Completado!")
        print(f"📈 Se agregaron {exercise_count} nuevos ejercicios")
        print(f"💪 Total de ejercicios en la base de datos: {total_exercises}")
        print(f"\n📊 Ejercicios por grupo muscular:")
        for grupo, count in exercises_by_group.items():
            print(f"   {grupo.upper():12}: {count:3d} ejercicios")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def create_admin_user():
    """Crear usuario administrador"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            print("✅ Usuario admin ya existe")
            return admin_user
        
        # Crear usuario admin
        admin_user = User(
            email="admin@gainzapi.com",
            username="admin",
            full_name="Administrador",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("✅ Usuario admin creado")
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creando admin: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def main():
    """Función principal"""
    print("🏋️ GAINZ API - Poblando base de datos con TODOS los ejercicios\n")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Poblar ejercicios basados en imágenes
    populate_all_exercises()
    
    # Crear usuario admin
    create_admin_user()
    
    print(f"\n✅ ¡Base de datos completamente poblada!")
    print(f"🚀 Ejecuta la API con: python main.py")
    print(f"📚 Documentación: http://localhost:8000/docs")

if __name__ == "__main__":
    main()