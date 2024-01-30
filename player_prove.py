import pygame
from setings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/character.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.health = 10
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.last_magma = None
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
                if sprite.rect.colliderect(self.rect):
                    if sprite.type != 'magma':  # Permitir paso por encima de magma
                        if self.direction.x > 0:  # Moving right
                            self.rect.right = sprite.rect.left
                        elif self.direction.x < 0:  # Moving left
                            self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if sprite.type != 'magma':  # Permitir paso por encima de magma
                        if self.direction.y > 0:  # Moving down
                            self.rect.bottom = sprite.rect.top
                        elif self.direction.y < 0:  # Moving up
                            self.rect.top = sprite.rect.bottom

    def check_magma_collision(self):
        current_magma = None
        for sprite in self.obstacles_sprites:
            if sprite.type == 'magma' and self.rect.colliderect(sprite.rect):
                current_magma = sprite
                break

        # Si el personaje entra en un nuevo bloque de lava
        if current_magma and current_magma != self.last_magma:
            self.health -= 2
            print(self.health)

        # Actualiza la última posición de lava
        self.last_magma = current_magma

    def update(self):
        self.input()
        self.move(self.speed)
        self.check_magma_collision()
