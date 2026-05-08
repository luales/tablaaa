import json
import os
import random
import time

CARPETA_DATOS = "datos_recibidos"

# Crear la carpeta si no existe
if not os.path.exists(CARPETA_DATOS):
    os.makedirs(CARPETA_DATOS)

print("Generando datos de prueba. Presiona Ctrl+C para detener.")

try:
    while True:
        for i in range(1, 11):
            # Para el PC 1 dejaremos por defecto 10651, para los demás será aleatorio
            score = 10651 if i == 1 else random.randint(1000, 25000)
            
            datos = {
                "alias": f"Jugador_{i}",
                "score": score
            }
            
            ruta_archivo = os.path.join(CARPETA_DATOS, f"pc{i}.json")
            
            # Escribir el archivo JSON
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo)
                
        print("Archivos JSON actualizados...")
        time.sleep(2) # Actualiza los puntajes falsos cada 2 segundos

except KeyboardInterrupt:
    print("\nGenerador de pruebas detenido.")