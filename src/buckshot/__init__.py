import pygame as py
from buckshot.config import BASE_DIR, ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH

class BuckShot:
# Initial Setup
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        py.display.set_caption("Buckshot")
        icon = py.image.load(ASSETS_DIR / "game_logo.png")
        py.display.set_icon(icon)