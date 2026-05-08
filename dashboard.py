import pygame
import json
import glob
import os
import time

# --- CONFIGURACIÓN ---
CARPETA_DATOS = "datos_recibidos" 
RUTA_FUENTE = os.path.join("fuentes", "arcade.ttf")

ANCHO_VENTANA = 1024
ALTO_VENTANA = 768
FPS = 60

# Colores
COLOR_FONDO = (15, 15, 25)
COLOR_TITULO = (0, 255, 255)
COLOR_ORO = (255, 215, 0)
COLOR_PLATA = (192, 192, 192)
COLOR_BRONCE = (205, 127, 50)
COLOR_TEXTO = (200, 200, 200)

def leer_puntuaciones():
    leaderboard = []
    archivos_json = glob.glob(os.path.join(CARPETA_DATOS, "*.json"))
    
    for ruta in archivos_json:
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                if "alias" in datos and "score" in datos:
                    leaderboard.append((datos["alias"], datos["score"]))
        except (json.JSONDecodeError, PermissionError, FileNotFoundError):
            continue 

    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard

def iniciar_dashboard():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Dashboard - Torneo Tetris")
    reloj = pygame.time.Clock()

    try:
        fuente_titulo = pygame.font.Font(RUTA_FUENTE, 50)
        fuente_ranking = pygame.font.Font(RUTA_FUENTE, 30)
    except:
        fuente_titulo = pygame.font.SysFont("consolas", 50, bold=True)
        fuente_ranking = pygame.font.SysFont("consolas", 30)

    ultimo_escaneo = 0
    intervalo_escaneo = 1.0 
    ranking_actual = []

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

        # Título
        texto_titulo = fuente_titulo.render("TOP RANKING TETRIS", True, COLOR_TITULO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, 80))
        pantalla.blit(texto_titulo, rect_titulo)
        pygame.draw.line(pantalla, COLOR_TITULO, (100, 140), (ANCHO_VENTANA - 100, 140), 3)

        # Renderizar jugadores
        pos_y_inicial = 200
        espaciado = 45

        for i, jugador in enumerate(ranking_actual[:10]):
            alias, score = jugador
            
            if i == 0: color_fila = COLOR_ORO
            elif i == 1: color_fila = COLOR_PLATA
            elif i == 2: color_fila = COLOR_BRONCE
            else: color_fila = COLOR_TEXTO

            texto_pos = fuente_ranking.render(f"{i+1}.", True, color_fila)
            texto_alias = fuente_ranking.render(f"{alias}", True, color_fila)
            texto_score = fuente_ranking.render(f"{score:06d}", True, color_fila)

            pantalla.blit(texto_pos, (200, pos_y_inicial + (i * espaciado)))
            pantalla.blit(texto_alias, (300, pos_y_inicial + (i * espaciado)))
            pantalla.blit(texto_score, (ANCHO_VENTANA - 350, pos_y_inicial + (i * espaciado)))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    # Crear la carpeta de recepción si no existe al abrir el programa
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)
    iniciar_dashboard()