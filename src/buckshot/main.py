import pygame as py
from pathlib import Path
from buckshot.scenes.main_menu import MainMenu

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / "assets"

py.init()

screen = py.display.set_mode((1200, 600))

py.display.set_caption("Buckshot")
icon = py.image.load(ASSETS_DIR / "game_logo.png")
py.display.set_icon(icon)

# Main menu
menu = MainMenu(screen, title="BuckShot")
selction = menu.run()

# Game loop
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Game logic

