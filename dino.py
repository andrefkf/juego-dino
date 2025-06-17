import pygame
import sys
import random
import time

pygame.init()
ANCHO, ALTO = 800, 300
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino sin Internet")
fuente = pygame.font.SysFont("Courier", 24)
reloj = pygame.time.Clock()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (120, 120, 120)

SUELO_Y = 250

def mostrar_texto(texto, x, y, centrado=False):
    render = fuente.render(texto, True, NEGRO)
    rect = render.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    pantalla.blit(render, rect)

def menu():
    seleccionado = 0
    opciones = ["Jugar", "Salir"]
    while True:
        pantalla.fill(BLANCO)
        mostrar_texto("===== Bienvenido a Dino =====", ANCHO // 2, 80, centrado=True)
        for i, opcion in enumerate(opciones):
            color = GRIS if i == seleccionado else NEGRO
            render = fuente.render(opcion, True, color)
            rect = render.get_rect(center=(ANCHO // 2, 140 + i * 40))
            pantalla.blit(render, rect)

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    return opciones[seleccionado]

        reloj.tick(15)

def pantalla_game_over(puntos, tiempo):
    seleccionado = 0
    opciones = ["Volver a jugar", "Salir"]
    while True:
        pantalla.fill(BLANCO)
        mostrar_texto("¡Perdiste!", ANCHO // 2, 80, centrado=True)
        mostrar_texto(f"Puntos: {puntos}", ANCHO // 2, 120, centrado=True)
        mostrar_texto(f"Tiempo: {tiempo:.2f} s", ANCHO // 2, 150, centrado=True)

        for i, opcion in enumerate(opciones):
            color = GRIS if i == seleccionado else NEGRO
            render = fuente.render(opcion, True, color)
            rect = render.get_rect(center=(ANCHO // 2, 200 + i * 40))
            pantalla.blit(render, rect)

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    return opciones[seleccionado]

        reloj.tick(15)

def jugar():
    dino = pygame.Rect(50, SUELO_Y - 40, 40, 40)
    vel_salto = 0
    en_suelo = True
    obstaculos = []
    suelo_lineas = [pygame.Rect(x, SUELO_Y, 20, 2) for x in range(0, ANCHO, 40)]
    puntos = 0
    velocidad = 8
    tiempo_inicio = time.time()

    nuevo_obstaculo = pygame.USEREVENT + 1
    pygame.time.set_timer(nuevo_obstaculo, 1400)

    while True:
        pantalla.fill(BLANCO)
        tiempo_actual = time.time() - tiempo_inicio

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == nuevo_obstaculo:
                tipo = random.choice(["bajo", "alto"])
                if tipo == "bajo":
                    obs = pygame.Rect(ANCHO, SUELO_Y - 30, 20, 30)
                else:
                    obs = pygame.Rect(ANCHO, SUELO_Y - 60, 20, 60)
                obstaculos.append(obs)

        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and en_suelo:
            vel_salto = -15
            en_suelo = False

        vel_salto += 1
        dino.y += vel_salto
        if dino.y >= SUELO_Y - 40:
            dino.y = SUELO_Y - 40
            en_suelo = True
            vel_salto = 0

        for obs in list(obstaculos):
            obs.x -= velocidad
            pygame.draw.rect(pantalla, NEGRO, obs)
            if obs.right < 0:
                obstaculos.remove(obs)
                puntos += 1
            if dino.colliderect(obs):
                return puntos, tiempo_actual

        for linea in suelo_lineas:
            linea.x -= velocidad
            if linea.right < 0:
                linea.x = ANCHO
            pygame.draw.rect(pantalla, GRIS, linea)

        pygame.draw.rect(pantalla, NEGRO, dino)

        mostrar_texto(f"Puntos: {puntos}", 10, 10)
        mostrar_texto(f"Tiempo: {tiempo_actual:.2f}s", 10, 40)

        pygame.display.flip()
        reloj.tick(60)

while True:
    opcion = menu()
    if opcion == "Jugar":
        puntos, tiempo = jugar()
        opcion_post = pantalla_game_over(puntos, tiempo)
        if opcion_post == "Salir":
            break
    else:
        break

pygame.quit()
