import pygame
import json
import glob
import os
import time

# --- CONFIGURACIÓN ---
CARPETA_DATOS = "datos_recibidos" 
RUTA_FUENTE = os.path.join("fuentes", "arcade.ttf")

# Resolución ampliada para acomodar 3 columnas
ANCHO_VENTANA = 1280  
ALTO_VENTANA = 768
FPS = 60

# Paleta de colores temáticos
COLOR_FONDO = (15, 15, 25)
COLOR_TITULO = (0, 255, 255)
COLOR_JUNIOR = (50, 255, 50)     # Verde neón para Junior
COLOR_SENIOR = (255, 50, 50)     # Rojo neón para Senior
COLOR_PROFES = (150, 50, 255)    # Púrpura neón para Profesores
COLOR_TEXTO = (200, 200, 200)

def leer_puntuaciones():
    """Lee y agrupa los puntajes por categoría"""
    # Estructura principal dividida en las 3 ramas
    categorias = {
        "Junior": [],
        "Senior": [],
        "Profesores": []
    }
    
    archivos_json = glob.glob(os.path.join(CARPETA_DATOS, "*.json"))
    
    for ruta in archivos_json:
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                
                # Leemos las llaves del nuevo diseño de código
                alias = datos.get("alias")
                high_score = datos.get("high_score")
                categoria = datos.get("categoria")
                
                # Clasificamos al jugador en su lista correspondiente
                if alias and high_score is not None and categoria in categorias:
                    categorias[categoria].append((alias, high_score))
                    
        except (json.JSONDecodeError, PermissionError, FileNotFoundError):
            continue 

    # Ordenar cada categoría de mayor a menor de forma independiente
    for cat in categorias:
        categorias[cat].sort(key=lambda x: x[1], reverse=True)
        
    return categorias

def iniciar_dashboard():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Ranking Torneo Tetris - Multicategoría")
    reloj = pygame.time.Clock()

    # Reducción leve del tamaño de fuente para que entren las 3 columnas
    try:
        fuente_titulo = pygame.font.Font(RUTA_FUENTE, 45)
        fuente_subtitulo = pygame.font.Font(RUTA_FUENTE, 25)
        fuente_ranking = pygame.font.Font(RUTA_FUENTE, 18)
    except:
        fuente_titulo = pygame.font.SysFont("consolas", 45, bold=True)
        fuente_subtitulo = pygame.font.SysFont("consolas", 25, bold=True)
        fuente_ranking = pygame.font.SysFont("consolas", 18)

    ultimo_escaneo = 0
    intervalo_escaneo = 1.0 
    ranking_actual = {"Junior": [], "Senior": [], "Profesores": []}

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False

        tiempo_actual = time.time()
        if tiempo_actual - ultimo_escaneo > intervalo_escaneo:
            ranking_actual = leer_puntuaciones()
            ultimo_escaneo = tiempo_actual

        pantalla.fill(COLOR_FONDO)

        # 1. Dibujar Título Principal
        texto_titulo = fuente_titulo.render("TOP RANKING TETRIS", True, COLOR_TITULO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, 50))
        pantalla.blit(texto_titulo, rect_titulo)
        pygame.draw.line(pantalla, COLOR_TITULO, (50, 90), (ANCHO_VENTANA - 50, 90), 3)

        # 2. Configuración geométrica de las 3 columnas
        # Se define el centro X de cada columna en la pantalla
        config_columnas = [
            ("Junior", COLOR_JUNIOR, ANCHO_VENTANA // 6),
            ("Senior", COLOR_SENIOR, ANCHO_VENTANA // 2),
            ("Profesores", COLOR_PROFES, 5 * (ANCHO_VENTANA // 6))
        ]

        pos_y_inicial = 180
        espaciado = 40

        # 3. Dibujar cada categoría y sus respectivos jugadores
        for categoria, color_cat, centro_x in config_columnas:
            # Subtítulo (ej. "--- Senior ---")
            texto_cat = fuente_subtitulo.render(f"--- {categoria} ---", True, color_cat)
            rect_cat = texto_cat.get_rect(center=(centro_x, 130))
            pantalla.blit(texto_cat, rect_cat)

            # Obtener la lista de jugadores de esa categoría
            jugadores = ranking_actual.get(categoria, [])
            
            # Limitar al Top 10 por categoría
            for i, jugador in enumerate(jugadores[:10]):
                alias, score = jugador
                
                texto_pos = fuente_ranking.render(f"{i+1}.", True, COLOR_TEXTO)
                # Recortar alias muy largos para que no invadan la columna vecina
                texto_alias = fuente_ranking.render(f"{alias[:8]}", True, COLOR_TEXTO) 
                texto_score = fuente_ranking.render(f"{score:06d}", True, color_cat)

                # Calcular coordenadas relativas al centro de la columna
                x_base = centro_x - 130
                pantalla.blit(texto_pos, (x_base, pos_y_inicial + (i * espaciado)))
                pantalla.blit(texto_alias, (x_base + 40, pos_y_inicial + (i * espaciado)))
                pantalla.blit(texto_score, (x_base + 170, pos_y_inicial + (i * espaciado)))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)
    iniciar_dashboard()