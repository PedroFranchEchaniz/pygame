import pygame
from setings import *
from coin import Coin
from potion import Potion
from bomb import Bomb

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites, collectible_sprites, level):
        super().__init__(groups)
        self.image = pygame.image.load('assets/character.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 10
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.last_magma = None
        self.obstacles_sprites = obstacles_sprites
        self.collectible_sprites = collectible_sprites
        self.level = level
        self.coins = 0
        self.bombs = 0
        self.starting_pos = pos

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        if keys[pygame.K_SPACE]:
            self.use_bomb()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() * speed
        self.rect.x += self.direction.x
        self.collision('horizontal')
        self.rect.y += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    # Cambia sprite.type por sprite.tile_type aquí
                    if sprite.tile_type != 'magma':
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left
                        elif self.direction.x < 0:
                            self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    # Y también cambia sprite.type por sprite.tile_type aquí
                    if sprite.tile_type != 'magma':
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                        elif self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom
    def check_death(self):
        if self.health <= 0:
            self.restart_game()

    def check_magma_collision(self):
        current_magma = None
        for sprite in self.obstacles_sprites:
            # Aquí cambiamos `sprite.type` por `sprite.tile_type`
            if sprite.tile_type == 'magma' and self.rect.colliderect(sprite.rect):
                current_magma = sprite
                break

        if current_magma and current_magma != self.last_magma:
            self.health -= 2
            print(self.health)

        self.last_magma = current_magma


        if current_magma and current_magma != self.last_magma:
            self.health -= 2
            print(self.health)


        self.last_magma = current_magma

    def check_potion_collision(self):
        for potion in self.get_colliding_sprites(Potion, self.collectible_sprites):
            self.health += 2
            potion.kill()

    def check_coin_collision(self):
        for coin in self.get_colliding_sprites(Coin, self.collectible_sprites):
            self.coins += 1
            coin.kill()

    def check_bomb_collision(self):
        # Este método se llamaría en la actualización del jugador para verificar si ha recogido una bomba.
        for bomb in self.get_colliding_sprites(Bomb, self.collectible_sprites):
            self.bombs += 1
            bomb.kill()

    def use_bomb(self):
        if self.bombs > 0:
            print("Usando bomba, bombas restantes:", self.bombs - 1)
            self.bombs -= 1

            # Área alrededor del jugador para considerar como adyacente
            adjacent_area = pygame.Rect(self.rect.x - TILESIZE, self.rect.y - TILESIZE,
                                        TILESIZE * 3, TILESIZE * 3)

            for tile in self.level.obstacles_sprites:
                if adjacent_area.colliderect(tile.rect):
                    print("Tile adyacente encontrado:", tile.rect.topleft, "de tipo:", tile.tile_type)
                    if tile.tile_type in ['wall_x', 'wall_y']:
                        print("Destruyendo tile:", tile.rect.topleft, "de tipo:", tile.tile_type)
                        tile.destroy()



    def get_colliding_sprites(self, sprite_type, group):
        return [sprite for sprite in group if isinstance(sprite, sprite_type) and self.rect.colliderect(sprite.rect)]



    def check_death(self):
        if self.health <= 0:
            self.restart_game()

    def restart_game(self):
        print("Has perdido. El juego se reiniciará.")
        self.health = 10
        self.coins = 0
        self.rect.topleft = self.starting_pos
        self.level.restart_level()

    def update(self):
        self.input()
        self.move(self.speed)
        self.check_magma_collision()
        self.check_potion_collision()
        self.check_coin_collision()
        self.check_death()
        self.check_bomb_collision()