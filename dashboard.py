import pygame
import json
import glob
import os
import time
from datetime import datetime  

# --- CONFIGURACIÓN ---
CARPETA_DATOS = "datos_guardados" 
RUTA_FUENTE = os.path.join("fuentes", "arcade.ttf")

# Resolución
ANCHO_VENTANA = 1280  
ALTO_VENTANA = 768
FPS = 60

# Paleta de colores temáticos
COLOR_FONDO = (15, 15, 25)
COLOR_TITULO = (0, 255, 255)
COLOR_JUNIOR = (50, 255, 50)     
COLOR_SENIOR = (255, 50, 50)     
COLOR_PROFES = (150, 50, 255)    
COLOR_TEXTO = (200, 200, 200)

def leer_puntuaciones():
    """Lee y agrupa los puntajes por categoría"""
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
                
                alias = datos.get("alias")
                high_score = datos.get("high_score")
                categoria = datos.get("categoria")
                
                if alias and high_score is not None and categoria in categorias:
                    categorias[categoria].append((alias, high_score))
                    
        except (json.JSONDecodeError, PermissionError, FileNotFoundError):
            continue 

    for cat in categorias:
        categorias[cat].sort(key=lambda x: x[1], reverse=True)
        
    return categorias

def iniciar_dashboard():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Ranking Torneo Tetris - Multicategoría")
    reloj = pygame.time.Clock()

    try:
        fuente_titulo = pygame.font.Font(RUTA_FUENTE, 45)
        fuente_subtitulo = pygame.font.Font(RUTA_FUENTE, 25) # <--- Esta es la fuente que usaremos para el reloj
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
        texto_titulo = fuente_titulo.render("TOP 10 PUNTAJES", True, COLOR_TITULO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, 50))
        pantalla.blit(texto_titulo, rect_titulo)
        pygame.draw.line(pantalla, COLOR_TITULO, (50, 90), (ANCHO_VENTANA - 50, 90), 3)

        # 2. Configuración geométrica de las 3 columnas
        config_columnas = [
            ("Junior", COLOR_JUNIOR, ANCHO_VENTANA // 6),
            ("Senior", COLOR_SENIOR, ANCHO_VENTANA // 2),
            ("Profesores", COLOR_PROFES, 5 * (ANCHO_VENTANA // 6))
        ]

        pos_y_inicial = 180
        espaciado = 40

        # 3. Dibujar cada categoría y sus respectivos jugadores
        for categoria, color_cat, centro_x in config_columnas:
            texto_cat = fuente_subtitulo.render(f"--- {categoria} ---", True, color_cat)
            rect_cat = texto_cat.get_rect(center=(centro_x, 130))
            pantalla.blit(texto_cat, rect_cat)

            jugadores = ranking_actual.get(categoria, [])
            
            for i, jugador in enumerate(jugadores[:10]):
                alias, score = jugador
                
                texto_pos = fuente_ranking.render(f"{i+1}.", True, COLOR_TEXTO)
                texto_alias = fuente_ranking.render(f"{alias[:8]}", True, COLOR_TEXTO) 
                texto_score = fuente_ranking.render(f"{score:06d}", True, color_cat)

                x_base = centro_x - 130
                pantalla.blit(texto_pos, (x_base, pos_y_inicial + (i * espaciado)))
                pantalla.blit(texto_alias, (x_base + 40, pos_y_inicial + (i * espaciado)))
                pantalla.blit(texto_score, (x_base + 170, pos_y_inicial + (i * espaciado)))

        
        hora_texto = datetime.now().strftime("%H:%M:%S") 
        # Renderiza usando la misma fuente que los subtítulos (tamaño 25)
        superficie_hora = fuente_subtitulo.render(hora_texto, True, COLOR_TITULO) 
        # Posiciona a 20 px del borde izquierdo y 40 px del borde inferior
        pantalla.blit(superficie_hora, (20, ALTO_VENTANA - 40))
        # ==========================================

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS, exist_ok=True)
    iniciar_dashboard()