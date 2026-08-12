import pygame as py
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS

class Player():
    def __init__(self, screen, x = -100, y = -180, flipped = False, health=5):

        # Player state
        self.health = health

        self.screen = screen
        self.x = x
        self.y = y
        self.flipped = flipped
        self.idle_frames = []
        frame_width = 128
        frame_height = 128
        self.current_frame = 0
        self.animation_timer = 0

        if not flipped:
            idle = py.image.load(ASSETS_DIR / "sprites" / "character1" / "idle.png").convert_alpha()
            idle_2 = py.image.load(ASSETS_DIR / "sprites" / "character1" / "idle_2.png").convert_alpha()

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
        if flipped:
            idle = py.image.load(ASSETS_DIR / "sprites" / "character2" / "idle.png").convert_alpha()
            idle = py.transform.flip(idle, True, False) 

            for i in range(4):
                frame = idle.subsurface(
                    (i * frame_width, 0, frame_width, frame_height)
                )
                frame = py.transform.scale(frame, (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 1.25))
    
                self.idle_frames.append(frame)

    def fire(self):
        """Perform the player's firing action."""
        return True

    def take_damage(self, amount=1):
        """Reduce the player's health."""
        if amount < 0:
            raise ValueError("Damage amount cannot be negative.")

        self.health = max(0, self.health - amount)

    def is_alive(self):
        """Return True if the player still has health."""
        return self.health > 0

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
       
