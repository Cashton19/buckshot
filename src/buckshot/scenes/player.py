import pygame as py
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS


class Player():
    def __init__(self, screen, x, y, flipped = False, health=5):

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
        self.is_animating = False
        self.idle_anims = py.image.load(ASSETS_DIR / "sprites" / "character2" / "idle.png").convert_alpha() if self.flipped else py.image.load(ASSETS_DIR / "sprites" / "character1" / "idle.png").convert_alpha()
        self.shoot_anims = py.image.load(ASSETS_DIR / "sprites" / "character2" / "shoot.png").convert_alpha() if self.flipped else py.image.load(ASSETS_DIR / "sprites" / "character1" / "shoot.png").convert_alpha()
        self.hurt_anims = py.image.load(ASSETS_DIR / "sprites" / "character2" / "Hurt.png").convert_alpha() if self.flipped else py.image.load(ASSETS_DIR / "sprites" / "character1" / "Hurt.png").convert_alpha()
        
        if self.flipped:                
            self.idle_anims = py.transform.flip(self.idle_anims, True, False) 
            self.shoot_anims = py.transform.flip(self.shoot_anims, True, False) 
            self.hurt_anims = py.transform.flip(self.hurt_anims, True, False) 

    def play_idle_anims(self):
        try:          
            for i in range(6) if not self.flipped else range(5, -1, -1):
                frame = self.idle_anims.subsurface(
                    (i * self.frame_width, 0, self.frame_width, self.frame_height)
                )
                frame = py.transform.scale_by(frame, 6)
                self.total_frames.append(frame)
        except Exception as e:
            print(f"Error : {e}")

    def play_shoot_anims(self):
        try:
            self.is_animating = True
            for i in range(4) if not self.flipped else range(3, -1, -1):
                frame = self.shoot_anims.subsurface(
                    (i * self.frame_width, 0, self.frame_width, self.frame_height)
                )
                frame = py.transform.scale_by(frame, 6)
                self.total_frames.append(frame)
        except Exception as e:
            print(f"Error : {e}")
            
    def play_hurt_anims(self):
        try:
            self.is_animating = True
            for i in range(3) if not self.flipped else range(2, -1, -1):
                frame = self.hurt_anims.subsurface(
                    (i * self.frame_width, 0, self.frame_width, self.frame_height)
                )
                frame = py.transform.scale_by(frame, 6)
                self.total_frames.append(frame)
        except Exception as e:
            print(f"Error : {e}")

    def stop_anims(self):
        self.total_frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.is_animating = False

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
       
