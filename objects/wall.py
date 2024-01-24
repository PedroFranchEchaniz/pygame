import pygame

class Walls:
    def __init__(self):
        self.walls = []

    def add_wall(self, x, y, width, height):
        self.walls.append({'rect': pygame.Rect(x, y, width, height)})

    def check_collision(self, player_rect):
        for wall in self.walls:
            if player_rect.colliderect(wall['rect']):
                return True
        return False