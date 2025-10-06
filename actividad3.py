import pygame, random
pygame.init()

ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("EcoRunner")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 40)

VERDE = (0, 200, 0)
GRIS = (80, 80, 80)
FONDO = (200, 255, 200)
NEGRO = (0, 0, 0)

jugador = pygame.Rect(100, 300, 40, 40)
salto = False
velocidad_salto = 0

obstaculos = []
puntos = 0
velocidad = 8
nivel = 1

pantalla_inicio = True
game_over = False
corriendo = True

def mostrar_texto(texto, tamano, color, y):
    fuente_tmp = pygame.font.Font(None, tamano)
    render = fuente_tmp.render(texto, True, color)
    pantalla.blit(render, ((ANCHO - render.get_width()) // 2, y))

en_juego = False
while corriendo:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            corriendo = False
        if e.type == pygame.KEYDOWN:
            if pantalla_inicio and e.key == pygame.K_SPACE:
                pantalla_inicio = False
                en_juego = True
                puntos = 0
                obstaculos.clear()
                jugador.y = 300
                velocidad = 8
                nivel = 1
            elif game_over and e.key == pygame.K_r:
                game_over = False
                en_juego = True
                puntos = 0
                obstaculos.clear()
                jugador.y = 300
                velocidad = 8
                nivel = 1
            elif e.key == pygame.K_ESCAPE:
                corriendo = False
            elif en_juego and not salto:
                salto = True
                velocidad_salto = -15

    if en_juego:
        if salto:
            jugador.y += velocidad_salto
            velocidad_salto += 1
            if jugador.y >= 300:
                jugador.y = 300
                salto = False

        if random.randint(1, 40) == 1:
            obstaculos.append(pygame.Rect(ANCHO, 320, 20, 30))

        for o in list(obstaculos):
            o.x -= velocidad
            if o.x < 0:
                obstaculos.remove(o)
                puntos += 1


        if puntos > 0 and puntos % 20 == 0:
            nivel = (puntos // 10) + 1
            velocidad = 8 + nivel * 2 

        for o in obstaculos:
            if jugador.colliderect(o):
                en_juego = False
                game_over = True

        
        pantalla.fill(FONDO)
        pygame.draw.rect(pantalla, VERDE, jugador)
        for o in obstaculos:
            pygame.draw.rect(pantalla, GRIS, o)

        texto = fuente.render(f"Puntos: {puntos}  Nivel: {nivel}", True, NEGRO)
        pantalla.blit(texto, (10, 10))

    elif pantalla_inicio:
        pantalla.fill(FONDO)
        mostrar_texto("🌱 ECO RUNNER 🌱", 60, VERDE, 120)
        mostrar_texto("Presiona ESPACIO para empezar", 40, NEGRO, 200)
        mostrar_texto("Evita los obstáculos y cuida el planeta", 30, NEGRO, 250)

    elif game_over:
        pantalla.fill(FONDO)
        mostrar_texto("💥 GAME OVER 💥", 60, (255, 0, 0), 120)
        mostrar_texto(f"Puntaje final: {puntos}", 40, NEGRO, 200)
        mostrar_texto("Presiona R para reiniciar o ESC para salir", 30, NEGRO, 260)

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
