import pygame
from tile import Tile
from entity import Entity

class Bomb(Entity):
    def __init__(self, pos, explosion_radius, all_sprites, obstacles_sprites, bomb_group, size=None):
        super().__init__(pos, [bomb_group, all_sprites], "assets/pngwing.com.png", size)
        self.explosion_radius = explosion_radius
        self.obstacles_sprites = obstacles_sprites

    def explode(self):
        print("Exploding bomb at:", self.rect.center)
        for sprite in self.obstacles_sprites:
            if isinstance(sprite, Tile) and sprite.destructible:
                distance = self.rect.center.distance_to(sprite.rect.center)
                if distance <= self.explosion_radius:
                    sprite.destroy()
        self.kill()