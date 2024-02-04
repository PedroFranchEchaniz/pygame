import pygame
from entity import Entity

class Potion(Entity):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, "assets/potion.png")
