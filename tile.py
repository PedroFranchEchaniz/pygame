import pygame
from setings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_type, obstacles_sprites):
        super().__init__(groups)
        self.tile_type = tile_type
        self.obstacles_sprites = obstacles_sprites
        self.load_image(tile_type)
        self.rect = self.image.get_rect(topleft=pos)

    def load_image(self, tile_type):
        if tile_type == 'wall_y':
            image_path = 'assets/brickx.png'
        elif tile_type == 'wall_x':
            image_path = 'assets/bricky.png'
        elif tile_type == 'magma':
            image_path = 'assets/magma.png'
        else:
            image_path = None

        if image_path:
            image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
        else:
            self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))  # Rellenar con transparente para tipos desconocidos

    def destroy(self):
        if self in self.obstacles_sprites:
            self.obstacles_sprites.remove(self)
            self.kill()