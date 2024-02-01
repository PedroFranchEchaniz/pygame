import pygame

class Suit(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("assets/flasks_3_4.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)