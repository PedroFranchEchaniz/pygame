import pygame

class Bomb (pygame.sprite.Sprite):
    def __init__(self, pos, groups, size=(20, 20)):
        super().__init__(groups)
        original_image = pygame.image.load("assets/pngwing.com.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect(topleft=pos)