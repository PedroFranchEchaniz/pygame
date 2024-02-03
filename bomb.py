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
        for sprite in self.all_sprites:
            if self.rect.center.distance_to(sprite.rect.center) <= self.explosion_radius:
                if isinstance(sprite, Tile):
                    sprite.destroy()
                elif isinstance(sprite, Bomb) and sprite != self:
                    sprite.explode()
        self.kill()