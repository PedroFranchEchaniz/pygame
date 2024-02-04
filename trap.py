import pygame
from setings import TILESIZE


class Trap(pygame.sprite.Sprite):
    def __init__(self, pos, groups, animation_frames, damage):
        super().__init__(groups)
        self.tile_type = 'trap'
        self.frames = self.load_frames(animation_frames)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.damage = damage
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 500
        self.animation_direction = 1

    def load_frames(self, animation_frames):
        adjusted_frames = [pygame.transform.scale(frame, (TILESIZE, TILESIZE)) for frame in animation_frames]
        return adjusted_frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += self.animation_direction
            if self.current_frame >= len(self.frames):
                self.current_frame = len(self.frames) - 2
                self.animation_direction = -1
            elif self.current_frame < 0:
                self.current_frame = 1
                self.animation_direction = 1

            self.image = self.frames[self.current_frame]

    def update(self):
        self.animate()

    def is_active(self):
        active_frame = [3]
        margin_frame = [0, 1, 2]
        return self.current_frame in active_frame and self.current_frame not in margin_frame

    def reset(self):
        self.current_frame = 0
        self.animation_direction = 1
        self.last_update = pygame.time.get_ticks()
