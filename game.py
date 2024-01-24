import pygame
from objects.player import Player

pygame.init()

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen_height = 650
surface_width = 800
surface_height = 600
character = pygame.image.load('assets/character.png')
room = pygame.image.load('assets/room.png')
wall_horizontal_sprite = pygame.image.load('assets/wall_vertical.png')
wall_vertical_sprite = pygame.image.load('assets/wall_horizontal.png')

player = Player(character)
walls = []

# Crear un pasillo horizontal
for i in range(10):
    wall_rect = pygame.Rect(i * 50, 200, 50, 20)
    walls.append(wall_rect)

# Crear una sala al final del pasillo
wall_rect = pygame.Rect(500, 200, 20, 100)
walls.append(wall_rect)

running = True
surface = pygame.Surface((surface_width, surface_height))
screen = pygame.display.set_mode((surface_width, screen_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.is_moving_right = True
            elif event.key == pygame.K_LEFT:
                player.is_moving_left = True
            elif event.key == pygame.K_UP:
                player.is_moving_up = True
            elif event.key == pygame.K_DOWN:
                player.is_moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.is_moving_right = False
            elif event.key == pygame.K_LEFT:
                player.is_moving_left = False
            elif event.key == pygame.K_UP:
                player.is_moving_up = False
            elif event.key == pygame.K_DOWN:
                player.is_moving_down = False

    player.update_position()

    player_rect = player.get_rect()
    collision = False
    for wall_rect in walls:
        if player_rect.colliderect(wall_rect):
            collision = True
            player.position[0] -= player.speed if player.is_moving_right else 0
            player.position[0] += player.speed if player.is_moving_left else 0
            player.position[1] -= player.speed if player.is_moving_down else 0
            player.position[1] += player.speed if player.is_moving_up else 0

    screen.fill((0, 0, 0))
    screen.blit(room, (0, 0))

    # Dibujar las paredes
    for wall_rect in walls:
        if wall_rect.width > wall_rect.height:
            screen.blit(wall_horizontal_sprite, (wall_rect.x, wall_rect.y))
        else:
            screen.blit(wall_vertical_sprite, (wall_rect.x, wall_rect.y))

    screen.blit(player.sprite, (player.position[0], player.position[1]))

    if collision:
        pygame.draw.rect(screen, RED, player_rect, 2)

    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()