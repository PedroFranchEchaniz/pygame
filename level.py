from tile import Tile
from player_prove import *
from player_prove import Player

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        # sptite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprite setuo
        self.create_map()

    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites, self.obstacles_sprites])
                if col == 'y':
                    Tile((x,y), [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()