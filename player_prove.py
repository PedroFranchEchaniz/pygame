import pygame
from setings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/character.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacles_sprites = obstacles_sprites

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
                if sprite.rect != self.rect and self.rect.colliderect(sprite.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.rect != self.rect and self.rect.colliderect(sprite.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def water(self):
        if self.obstacles_sprites

    def update(self):
        self.input()
        self.move(self.speed)
