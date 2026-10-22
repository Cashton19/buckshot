import pygame as py
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS

class player_text():
    def __init__(self, screen):
        self.screen = screen
        self.margin_x = int(SCREEN_WIDTH * 0.05)
        self.top_padding = int(SCREEN_HEIGHT * 0.03)
        self.font = py.font.Font(ASSETS_DIR / "fonts" / "Pixeltype.ttf", 32)
        self.player_name_left = self.font.render("Player 1", True, (255, 255, 255))
        self.player_name_right = self.font.render("Player 2", True, (255, 255, 255))
        
    def highlight(self, player_index):
        if player_index == 0:
            self.player_name_left = self.font.render("Player 1", True, (255, 0, 0))
            self.player_name_right = self.font.render("Player 2", True, (255, 255, 255))
        else:
            self.player_name_left = self.font.render("Player 1", True, (255, 255, 255))
            self.player_name_right = self.font.render("Player 2", True, (255, 0, 0)) 
    
    def update(self):
        self.player_name_left_rect = self.player_name_left.get_rect(
            topleft=(self.margin_x, self.top_padding)
        )
        self.player_name_right_rect = self.player_name_right.get_rect(
            topright=(
                SCREEN_WIDTH - self.margin_x,
                self.top_padding
                )  
        )
        
    def draw(self):
        self.screen.blit(self.player_name_left, self.player_name_left_rect)
        self.screen.blit(self.player_name_right, self.player_name_right_rect)