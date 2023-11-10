import pygame
import sys



# Налаштування гри
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
TRAP_SIZE = 20
PLAYER_SPEED = 5

# Кольори
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ініціалізація Pygame
pygame.init()

# Створення вікна гри
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Створення гравця і пасток
player = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)
traps = []

# Головний цикл гри
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Рух гравця
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_w]:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player.y += PLAYER_SPEED

    # Розміщення пасток
    if keys[pygame.K_SPACE]:
        trap = pygame.Rect(player.x, player.y, TRAP_SIZE, TRAP_SIZE)
        traps.append(trap)

    # Оновлення вікна гри
    window.fill(WHITE)
    pygame.draw.rect(window, RED, player)
    for trap in traps:
        pygame.draw.rect(window, RED, trap)
    pygame.display.update()
