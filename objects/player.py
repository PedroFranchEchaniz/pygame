import pygame
class Player:
    def __init__(self, sprite):
        self.position = [100, 60]
        self.speed = 5
        self.health = 10
        self.sprite = sprite
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_moving_up = False
        self.is_moving_down = False

    def update_position(self):
        if self.is_moving_right:
            self.move_right()
        elif self.is_moving_left:
            self.move_left()
        elif self.is_moving_up:
            self.move_up()
        elif self.is_moving_down:
            self.move_down()
        self.check_water_collision()

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def check_water_collision(self):
        # Suponiendo que los sprites de agua tienen una etiqueta o atributo para identificarlos
        for obstacle in self.obstacles_sprites:
            if obstacle.type == 'water' and self.get_rect().colliderect(obstacle.rect):
                self.health -= 2
                print("pierde vida")

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.sprite.get_width(), self.sprite.get_height())