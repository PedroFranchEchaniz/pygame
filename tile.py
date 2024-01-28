import pygame
from setings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_type):
            super().__init__(groups)
            if tile_type == 'wall_x':
                image = pygame.image.load('assets/bricky.png').convert_alpha()
                self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
            elif tile_type == 'wall_y':
                image = pygame.image.load('assets/brickx.png').convert_alpha()
                self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
            self.rect = self.image.get_rect(topleft=pos)
