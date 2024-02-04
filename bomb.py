import pygame
from tile import Tile

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, explosion_radius, all_sprites, obstacles_sprites, bomb_group):
        super().__init__(bomb_group, all_sprites)
        self.explosion_radius = explosion_radius
        self.all_sprites = all_sprites
        self.obstacles_sprites = obstacles_sprites
        self.image = pygame.Surface((20, 20))  # Temporal, usa una imagen adecuada
        self.image.fill((255, 0, 0))  # Temporal, usa una imagen adecuada
        self.rect = self.image.get_rect(center=pos)

    def explode(self):
        print("Exploding bomb at:", self.rect.center)
        for sprite in self.obstacles_sprites:
            if isinstance(sprite, Tile) and sprite.destructible:
                distance = self.rect.center.distance_to(sprite.rect.center)
                if distance <= self.explosion_radius:
                    sprite.destroy()  # Esto debería llamarse
        self.kill()