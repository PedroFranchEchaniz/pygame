import pygame
from tile import Tile

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, explosion_radius, all_sprites, obstacles_sprites, bomb_group):
        super().__init__(bomb_group, all_sprites)
        self.explosion_radius = explosion_radius
        self.all_sprites = all_sprites
        self.obstacles_sprites = obstacles_sprites
        self.image = pygame.image.load("assets/pngwing.com.png").convert_alpha()
        new_size = (20, 20)
        self.image = pygame.transform.scale(self.image, new_size)

        self.rect = self.image.get_rect(center=pos)

    def explode(self):
        print("Exploding bomb at:", self.rect.center)
        for sprite in self.obstacles_sprites:
            if isinstance(sprite, Tile) and sprite.destructible:
                distance = self.rect.center.distance_to(sprite.rect.center)
                if distance <= self.explosion_radius:
                    sprite.destroy()  # Esto debería llamarse
        self.kill()