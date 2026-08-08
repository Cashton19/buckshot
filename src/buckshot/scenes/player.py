import pygame as py
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS

class Player():
    def __init__(self, screen):
        self.screen = screen
        self.x = -100
        self.y = -180

        self.idle_frames = []


        idle = py.image.load(ASSETS_DIR / "sprites" / "character1" / "idle.png").convert_alpha()
        idle_2 = py.image.load(ASSETS_DIR / "sprites" / "character1" / "idle_2.png").convert_alpha()
        
        frame_width = 128
        frame_height = 128

        for i in range(4):
            frame = idle.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            )
            frame = py.transform.scale(frame, (SCREEN_WIDTH // 1.9, SCREEN_HEIGHT * 1.25))

            self.idle_frames.append(frame)
        for i in range(11):
            frame = idle_2.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            )
            frame = py.transform.scale(frame, (SCREEN_WIDTH // 1.9, SCREEN_HEIGHT * 1.25))


            self.idle_frames.append(frame)

        self.current_frame = 0
        self.animation_timer = 0
    def update(self):
        self.animation_timer += 1

        if self.animation_timer >= 10:
            self.animation_timer = 0

            self.current_frame += 1

            if self.current_frame >= len(self.idle_frames):
                self.current_frame = 0
    def draw(self):
        self.screen.blit(
            self.idle_frames[self.current_frame],
            (self.x, self.y)
        )
