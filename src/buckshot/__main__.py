import pygame as py
from buckshot.config import BASE_DIR, ASSETS_DIR
from buckshot import BuckShot
from buckshot.scenes.main_menu import MainMenu
from buckshot.scenes.game_environment import GameEnvironment

# Initialize pygame
game = BuckShot()

# Main menu
menu = MainMenu(game.screen, title="BuckShot")
selection = menu.run()

# Game
if selection == "play":
    ge = GameEnvironment(game.screen)
    ge.run()

elif selection == "play":
    GameEnvironment(game.screen)

elif selection == "online":
    ...



