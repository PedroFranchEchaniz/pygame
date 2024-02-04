import pygame
from setings import *  # Asegúrate de que este archivo exista y esté correctamente configurado
from coin import Coin
from potion import Potion
from bomb import Bomb
from suit import Suit


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites, collectible_sprites, level, trap_group):
        super().__init__(groups)
        self.image = pygame.image.load('assets/character.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 10
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.obstacles_sprites = obstacles_sprites
        self.collectible_sprites = collectible_sprites
        self.level = level
        self.coins = 0
        self.bombs = 0
        self.has_suit = False
        self.starting_pos = pos
        self.space_pressed = False
        self.anim_index = 0
        self.anim_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.anim_direction = 'down'
        self.load_animations()
        self.trap_group = trap_group

    def load_animations(self):
        new_size = (40, 40)
        self.animations = {
            'down': [
                pygame.transform.scale(pygame.image.load(f'assets/character_down_{i}.png').convert_alpha(), new_size)
                for i in range(4)],
            'up': [pygame.transform.scale(pygame.image.load(f'assets/character_up_{i}.png').convert_alpha(), new_size)
                   for i in range(4)],
            'left': [
                pygame.transform.scale(pygame.image.load(f'assets/character_left_{i}.png').convert_alpha(), new_size)
                for i in range(4)],
            'right': [
                pygame.transform.scale(pygame.image.load(f'assets/character_right_{i}.png').convert_alpha(), new_size)
                for i in range(4)],
        }
        self.anim_direction = 'down'
        self.anim_index = 0
        self.image = self.animations[self.anim_direction][self.anim_index]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        if self.direction.x > 0:
            self.anim_direction = 'right'
        elif self.direction.x < 0:
            self.anim_direction = 'left'
        if self.direction.y > 0:
            self.anim_direction = 'down'
        elif self.direction.y < 0:
            self.anim_direction = 'up'

        if keys[pygame.K_SPACE]:
            if not self.space_pressed:
                self.use_bomb()
                self.space_pressed = True
        else:
            self.space_pressed = False

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 * self.anim_speed:
            self.last_update = now
            self.anim_index = (self.anim_index + 1) % len(self.animations[self.anim_direction])
            self.image = self.animations[self.anim_direction][self.anim_index]

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.rect.x += self.direction.x * speed
            self.collision('horizontal')
            self.rect.y += self.direction.y * speed
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
            if sprite.tile_type == 'magma' and self.rect.colliderect(sprite.rect):
                current_magma = sprite
                break

        if current_magma and current_magma != self.last_magma:
            if not self.has_suit:
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
        for bomb in self.get_colliding_sprites(Bomb, self.collectible_sprites):
            self.bombs += 1
            bomb.kill()

    def use_bomb(self):
        if self.bombs > 0:
            print("Usando bomba, bombas restantes:", self.bombs - 1)
            self.bombs -= 1


            adjacent_area = pygame.Rect(self.rect.x - TILESIZE, self.rect.y - TILESIZE,
                                        TILESIZE * 3, TILESIZE * 3)

            for tile in self.level.obstacles_sprites:
                if adjacent_area.colliderect(tile.rect) and tile.destructible:
                    print("Tile adyacente encontrado:", tile.rect.topleft, "de tipo:", tile.tile_type)
                    print("Destruyendo tile:", tile.rect.topleft, "de tipo:", tile.tile_type)
                    tile.destroy()

    def check_suit_collision(self):
        for suit in self.get_colliding_sprites(Suit, self.collectible_sprites):
            self.has_suit = True
            suit.kill()

    def get_colliding_sprites(self, sprite_type, group):
        return [sprite for sprite in group if isinstance(sprite, sprite_type) and self.rect.colliderect(sprite.rect)]


    def check_death(self):
        if self.health <= 0:
            self.restart_game()

    def check_trap_collision(self):
        hits = pygame.sprite.spritecollide(self, self.level.trap_group, False)
        for trap in hits:
            if trap.is_active():
                self.health -= trap.damage
                print(f"Vida restante: {self.health}")

    def restart_game(self):
        print("Has perdido. El juego se reiniciará.")
        self.health = 10
        self.coins = 0
        self.rect.topleft = self.starting_pos
        self.level.restart_level()

    def update(self):
        self.input()
        if self.direction.magnitude() != 0:  # Si hay movimiento, actualiza la animación
            self.update_animation()
        self.move(self.speed)
        self.check_magma_collision()
        self.check_potion_collision()
        self.check_coin_collision()
        self.check_death()
        self.check_bomb_collision()
        self.check_suit_collision()
        self.check_trap_collision()