import pygame

class Entity(pygame.sprite.Sprite):
    default_size = (20, 20)

    def __init__(self, pos, groups, image_path, size=None):
        super().__init__(groups)
        if size is None:
            size = Entity.default_size
        self._load_image(image_path, size)
        self.rect = self.image.get_rect(topleft=pos)

    def _load_image(self, image_path, size):
        image = pygame.image.load(image_path).convert_alpha() if image_path else pygame.Surface(size, pygame.SRCALPHA)
        self.image = pygame.transform.scale(image, size)