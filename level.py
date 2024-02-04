import pygame.image
import random

from tile import Tile
from player_prove import *
from player_prove import Player
from potion import Potion
from coin import Coin
from bomb import Bomb
from suit import Suit
from trap import Trap

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()

        self.map_data, self.object_counts = self.read_map_and_objects('map/map.txt')

        self.total_coins = sum(value for key, value in self.object_counts.items() if key == 'd')

        self.free_spaces = []
        self.trap_group = pygame.sprite.Group()  # Asegúrate de que esto está presente
        self.create_map()
        self.place_objects()
        self.player_won = False

    def draw_ui(self):
        font = pygame.font.Font(None, 30)  # Crea una fuente

        health_text = font.render(f"Salud: {self.player.health}", True, (255, 255, 255))
        self.display_surface.blit(health_text, (10, 10))

        bombs_text = font.render(f"Bombas: {self.player.bombs}", True, (255, 255, 255))
        self.display_surface.blit(bombs_text, (10, 40))

        coins_text = font.render(f"Monedas: {self.player.coins}", True, (255, 255, 255))
        self.display_surface.blit(coins_text, (10, 70))


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
        for row_index, row in enumerate(WORLD_MAP2):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'wall_y', self.obstacles_sprites, destructible= False)
                elif col == 'y':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'wall_x', self.obstacles_sprites, destructible= False)
                elif col == 'z':  # Paredes destructibles
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'wall_breakable', self.obstacles_sprites, destructible=True)
                elif col == 'w':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'magma', self.obstacles_sprites, destructible=False)
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites, self.collectible_sprites, self, self.trap_group)
                    self.player.coins = 0
                elif col == 'k':
                    trap_frames = [pygame.image.load(f'assets/trap_state_{i}.png').convert_alpha() for i in range(4)]
                    Trap((x, y), [self.visible_sprites, self.trap_group], trap_frames, damage=1)
                elif col == ' ':
                    self.free_spaces.append((x, y))

    def place_objects(self):
        for obj_type, count in self.object_counts.items():
            for _ in range(count):
                if self.free_spaces:
                    # Elige una posición aleatoria de los espacios libres disponibles
                    pos = random.choice(self.free_spaces)
                    # Remueve la posición elegida de la lista de espacios libres para evitar colocar otro objeto allí
                    self.free_spaces.remove(pos)

                    # Crea los objetos en la posición elegida
                    if obj_type == 'o':
                        Potion(pos, [self.visible_sprites, self.collectible_sprites])
                    elif obj_type == 'd':
                        Coin(pos, [self.visible_sprites, self.collectible_sprites])
                    elif obj_type == 'b':
                        Bomb(pos, [self.visible_sprites, self.collectible_sprites], self.visible_sprites,
                             self.obstacles_sprites, self.collectible_sprites)
                    elif obj_type == 't':
                        Suit(pos, [self.visible_sprites, self.collectible_sprites])
                    # Asegúrate de que estas posiciones estén efectivamente dentro de los límites establecidos por las paredes 'x' e 'y'

    def restart_level(self):
        self.visible_sprites.empty()
        self.obstacles_sprites.empty()
        self.collectible_sprites.empty()
        self.free_spaces.clear()
        self.create_map()
        self.place_objects()
        self.player.coins = 0
        self.player.health = 10
        self.player.rect.topleft = self.player.starting_pos
        self.player_won = False

    def run(self):
        self.visible_sprites.curstom_draw(self.player)
        self.visible_sprites.update()
        self.draw_ui()
        self.check_win()
        if self.player_won:
            self.display_victory_message()

    def check_win(self):
        if self.player.coins == self.total_coins:
            self.player_won = True
            pygame.time.wait(2000)
            self.display_victory_message()
            self.restart_level()

    def display_victory_message(self):
        font = pygame.font.Font(None, 50)

        text_surface = font.render("¡Has ganado!", True, (255, 255, 255))

        screen_width, screen_height = self.display_surface.get_size()
        text_width, text_height = text_surface.get_size()

        x = (screen_width - text_width) // 2
        y = (screen_height - text_height) // 2

        self.display_surface.blit(text_surface, (x, y))

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