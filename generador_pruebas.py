import json
import os
import random
from datetime import datetime
import time

CARPETA_DATOS = "datos_guardados"

# Esta línea creará la carpeta solo si no existe, evitando el WinError 183
os.makedirs(CARPETA_DATOS, exist_ok=True)

print("Generando perfiles multicategoría. Presiona Ctrl+C para detener.")

categorias_disponibles = ["Junior", "Senior", "Profesores"]

try:
    while True:
        for i in range(1, 16): 
            # Dejamos 10651 por defecto para el primer registro, aleatorio para el resto
            score = 10651 if i == 1 else random.randint(1000, 25000)
            
            categoria_asignada = categorias_disponibles[i % 3] 
            
            datos = {
                "alias": f"PLY_{i}",
                "nombre_real": f"Jugador Ficticio {i}",
                "colegio": "Instituto Central",
                "edad": 15,
                "categoria": categoria_asignada,
                "high_score": score,
                "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            ruta_archivo = os.path.join(CARPETA_DATOS, f"score_PLY_{i}.json")
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4)
                
        print("Archivos JSON de prueba actualizados...")
        time.sleep(2)

except KeyboardInterrupt:
    print("\nGenerador de pruebas detenido.")