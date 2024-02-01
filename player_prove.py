import pygame
from setings import *
from coin import Coin
from potion import Potion

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
        self.starting_pos = pos

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

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
                    if sprite.type != 'magma':
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left
                        elif self.direction.x < 0:
                            self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if sprite.type != 'magma':
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
            if sprite.type == 'magma' and self.rect.colliderect(sprite.rect):
                current_magma = sprite
                break


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

    def get_colliding_sprites(self, sprite_type, group):
        return [sprite for sprite in group if isinstance(sprite, sprite_type) and self.rect.colliderect(sprite.rect)]

    def update(self):
        self.input()
        self.move(self.speed)
        self.check_magma_collision()
        self.check_potion_collision()
        self.check_coin_collision()
        self.check_death()

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