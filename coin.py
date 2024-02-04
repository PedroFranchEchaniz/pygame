import pygame
from entity import Entity

class Coin (Entity):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, "assets/coin_4.png")
