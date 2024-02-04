import pygame
from setings import TILESIZE


class Trap(pygame.sprite.Sprite):
    def __init__(self, pos, groups, animation_frames, damage):
        super().__init__(groups)
        super().__init__(groups)
        self.tile_type = 'trap'
        self.frames = self.load_frames(animation_frames)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.damage = damage
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 500
        self.active_frame = len(self.frames) - 1
        self.is_up = False

    def load_frames(self, animation_frames):
        adjusted_frames = [pygame.transform.scale(frame, (TILESIZE, TILESIZE)) for frame in animation_frames]
        return adjusted_frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == self.active_frame:
                self.is_up = True
            elif self.current_frame >= len(self.frames):
                self.current_frame = 0
                self.is_up = False
            self.image = self.frames[self.current_frame]

    def update(self):
        self.animate()

    def is_active(self):
        return self.is_up

    def reset(self):
        self.current_frame = 0
        self.animation_direction = 1
        self.last_update = pygame.time.get_ticks()
