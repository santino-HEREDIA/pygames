import pygame
pygame.init()

pantalla = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Recolector Verde")

verde = (0, 200, 0)
marron = (100, 50, 0)
cielo = (135, 206, 235)

jugador = pygame.Rect(300, 200, 40, 40)
basura = pygame.Rect(100, 100, 20, 20)

fuente = pygame.font.Font(None, 36)

corriendo = True
puntos = 0

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador.x -= 1
    if teclas[pygame.K_RIGHT]:
        jugador.x += 1
    if teclas[pygame.K_UP]:
        jugador.y -= 1
    if teclas[pygame.K_DOWN]:
        jugador.y += 1

    pantalla.fill(cielo)
    pygame.draw.rect(pantalla, marron, basura)
    pygame.draw.rect(pantalla, verde, jugador)

    if jugador.colliderect(basura):
        puntos = +1
        print("¡El planeta te lo agradece!")
        basura.x, basura.y = -100, -100  

    texto = fuente.render(f"Puntos: {puntos}", True, verde)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()
