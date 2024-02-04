from io import open

WIDTH = 1280
HEIGTH = 720
FSP = 60
TILESIZE = 64

with open('map/map.txt', 'r') as file:
    WORLD_MAP2 = [list(line.strip()) for line in file]



