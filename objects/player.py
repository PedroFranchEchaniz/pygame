import pygame
class Player:
    def __init__(self, sprite):
        self.position = [100, 60]
        self.speed = 5
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

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.sprite.get_width(), self.sprite.get_height())