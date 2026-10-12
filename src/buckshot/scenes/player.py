import pygame as py
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS


class Player():
    def __init__(self, screen, x, y, path, flipped = False, health=5):

        # Player state
        self.health = health
        self.max_health = health
        self.screen = screen
        self.x = x
        self.y = y
        self.flipped = flipped
        self.total_frames = []
        self.frame_width = 128.0
        self.frame_height = 128.0
        self.current_frame = 0
        self.animation_timer = 0
        self.path = path


    def play_idle_anims(self):
        try:
            idle = py.image.load(self.path).convert_alpha()
            
            if self.flipped:                
                idle = py.transform.flip(idle, True, False) 

            for i in range(6):
                frame = idle.subsurface(
                    (i * self.frame_width, 0, self.frame_width, self.frame_height)
                )
                frame = py.transform.scale_by(frame, 5)
                self.total_frames.append(frame)
        except Exception as e:
            print("Error : {e}")

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

            if self.current_frame >= len(self.total_frames):
                self.current_frame = 0

    def draw(self):
        if not self.total_frames:
            return
        self.screen.blit(
            self.total_frames[self.current_frame],
            (self.x, self.y)
        )
       
