import pygame.image
import random

from tile import Tile
from player_prove import *
from player_prove import Player
from potion import Potion

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()


        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.map_data, self.object_counts = self.read_map_and_objects('map/map.txt')

        self.free_spaces = []

        self.create_map()
        self.place_objects()

    def read_map_and_objects(self, filename):
        with open(filename, 'r') as file:
            object_line = file.readline().strip()
            map_data = [list(line.strip()) for line in file]

        object_counts = self.parse_object_line(object_line)
        return map_data, object_counts

    def parse_object_line(self, line):
        parts = line.split(',')
        object_counts = {}
        for part in parts:
            key, value = part.strip().split('=')
            object_counts[key] = int(value)
        return object_counts




    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP2):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'wall_y')
                if col == 'y':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'wall_x')
                if col == 'w':
                    Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'magma')
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
                if col == ' ':
                    self.free_spaces.append((x, y))

    def place_objects(self):
        for obj_type, count in self.object_counts.items():
            for _ in range(count):
                if self.free_spaces:
                    pos = random.choice(self.free_spaces)
                    self.free_spaces.remove(pos)
                    if obj_type == 'o':
                        Potion(pos, [self.visible_sprites])


    def run(self):
        self.visible_sprites.curstom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_with = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()


    def curstom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_with
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            if sprite != player:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

            offset_pos = player.rect.topleft - self.offset
            self.display_surface.blit(player.image, offset_pos)