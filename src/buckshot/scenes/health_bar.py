import pygame as py
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS

class health_bar():
    def __init__(self,screen, flipped = False):
    # loading health bar
        self.screen = screen
        self.flipped = flipped
        self.margin_x = int(SCREEN_WIDTH * 0.05)
        health_bar_width = int(SCREEN_WIDTH * 0.38)        
        original_health_bar = py.image.load(
            ASSETS_DIR / "ui" / "health_bar" / "health_bar.png"
        ).convert_alpha()
        original_depleted = py.image.load(
            ASSETS_DIR / "ui" / "health_bar" / "health_bar_depleted.png"
        ).convert_alpha()

        health_bar_height = int(
            original_health_bar.get_height()
            * (health_bar_width / original_health_bar.get_width())
        )
        self.health_bar = py.transform.smoothscale(
            original_health_bar,
            (health_bar_width, health_bar_height)
        )
        self.health_bar_depleted = py.transform.smoothscale(
            original_depleted,
            (health_bar_width, health_bar_height)
        )       
        player_text_space = int(SCREEN_HEIGHT * 0.08)
        health_bar_y = player_text_space + 10
        
        
        self.health_bar_rect = self.health_bar.get_rect(
            topleft=(self.margin_x, health_bar_y)
        )
        self.health_bar_right_rect = self.health_bar.get_rect(
            topright=(
                SCREEN_WIDTH - self.margin_x + 10,
                health_bar_y
            )            
        )
        
    
        
    def update(self):
        pass
    
    def draw(self, ratio):
        width = int(self.health_bar_rect.width * ratio)
        
        if self.flipped:
            self.screen.blit(self.health_bar_depleted, self.health_bar_right_rect)
            self.screen.blit(
                self.health_bar, 
                self.health_bar_right_rect, 
                (0, 0, width, self.health_bar_right_rect.height)
            )
        else:
            self.screen.blit(self.health_bar_depleted, self.health_bar_rect)
            self.screen.blit(
                self.health_bar, 
                self.health_bar_rect, 
                (0, 0, width, self.health_bar_rect.height)
            )