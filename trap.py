import pygame


class Trap(pygame.sprite.Sprite):
    def __init__(self, pos, groups, animation_frames, damage):
        super().__init__(groups)
        self.tile_type = 'trap'
        self.frames = animation_frames  # Lista de imágenes para la animación
        self.current_frame = 0
        self.image = self.frames[self.current_frame]  # Imagen actual mostrada
        self.rect = self.image.get_rect(topleft=pos)
        self.damage = damage
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Ajusta para controlar la velocidad de animación
        self.active_frame = len(self.frames) - 1  # Índice del frame donde las picas están completamente fuera
        self.animation_direction = 1  # Comienza animando hacia adelante

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            # Actualiza el frame actual basado en la dirección de la animación
            self.current_frame += self.animation_direction

            # Invierte la animación si alcanza el final o el inicio
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
        # La trampa está activa solo en el frame específico
        return self.current_frame == self.active_frame