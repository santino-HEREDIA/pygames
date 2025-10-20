import pygame
import random
import os

pygame.init()

try:
    pygame.mixer.init()
    MIXER_OK = True
except Exception:
    MIXER_OK = False

WIDTH, HEIGHT = 600, 400
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stop CO")
fuente = pygame.font.Font(None, 36)
reloj = pygame.time.Clock()

auto = pygame.Rect(300, 350, 50, 30)
humo = pygame.Rect(random.randint(0, WIDTH - 20), 0, 20, 20)
puntos = 0

MUSIC_FILE = "background.mp3"  # Archivo MP3 en la misma carpeta
if MIXER_OK and os.path.exists(MUSIC_FILE):
    try:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)  # loop infinito
    except Exception as e:
        print(f"No se pudo reproducir {MUSIC_FILE}: {e}")
else:
    print(f"Aviso: no se encontró '{MUSIC_FILE}' o el mezclador falló.")


corriendo = True
game_over = False

COLOR_CIELO = (180, 220, 255)
COLOR_AUTO = (0, 200, 0)
COLOR_HUMO = (80, 80, 80)
COLOR_TEXTO = (0, 0, 0)


while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN and game_over:
            if evento.key == pygame.K_r:
                puntos = 0
                auto.x, auto.y = 300, 350
                humo.x, humo.y = random.randint(0, WIDTH - humo.width), 0
                game_over = False
            if evento.key == pygame.K_ESCAPE:
                corriendo = False

    if not game_over:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            auto.x -= 5
        if teclas[pygame.K_RIGHT]:
            auto.x += 5

        auto.x = max(0, min(auto.x, WIDTH - auto.width))

        humo.y += 5
        if humo.y > HEIGHT:
            humo.y = 0
            humo.x = random.randint(0, WIDTH - humo.width)
            puntos += 1

        if humo.y > HEIGHT:
            humo.y = 0
            humo.x = random.randint(0, WIDTH - humo.width)
            puntos -= 1

        if auto.colliderect(humo):
            print("💨 ¡Contaminación detectada!")
            puntos += 1
            humo.y = 0
            humo.x = random.randint(0, WIDTH - humo.width)

        if puntos >= 10:
            game_over = True

    pantalla.fill(COLOR_CIELO)
    pygame.draw.rect(pantalla, COLOR_AUTO, auto)
    pygame.draw.rect(pantalla, COLOR_HUMO, humo)

    texto = fuente.render(f"Puntos: {puntos}", True, COLOR_TEXTO)
    pantalla.blit(texto, (10, 10))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        pantalla.blit(overlay, (0, 0))
        msg = fuente.render("¡Felicidades! Llegaste a 10 puntos.", True, (255, 255, 255))
        sub = fuente.render("Presiona R para reiniciar o ESC para salir.", True, (255, 255, 255))
        pantalla.blit(msg, ((WIDTH - msg.get_width()) // 2, HEIGHT // 2 - 20))
        pantalla.blit(sub, ((WIDTH - sub.get_width()) // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
