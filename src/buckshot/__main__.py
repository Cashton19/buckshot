import pygame as py
import sys

from buckshot.config import FPS
from buckshot import BuckShot
from buckshot.scenes.main_menu import MainMenu
from buckshot.scenes.game_environment import GameEnvironment
from buckshot.logic.game_state import GameState

py.init()

def main():
    # Initialize game
    game = BuckShot()
    # Create scenes
    menu = MainMenu(
        game.screen,
        title="BuckShot"
    )
    # Initialize Logic
    game_state = GameState(game.screen)
    # Initialize Scene with Logic
    game_environment = GameEnvironment(
        game.screen,
        game_state
    )
    # Start at the main menu
    current_scene = "menu"
    while True:
        game.clock.tick(FPS)
        # -------------------------
        # Handle events
        # -------------------------
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if current_scene == "menu":
                selection = menu.handle_event(event)
                if selection == "play":
                    current_scene = "game"
                elif selection == "quit":
                    py.quit()
                    sys.exit()
            elif current_scene == "game":
                game_environment.handle_event(event)
        # -------------------------
        # Update
        # -------------------------
        if current_scene == "menu":
            menu.update()
        elif current_scene == "game":
            game_environment.update()
            game_state.update()
        # -------------------------
        # Draw
        # -------------------------
        if current_scene == "menu":
            menu.draw()
        elif current_scene == "game":
            game_environment.draw()
            game_state.draw()
            py.display.flip()
if __name__ == "__main__":
    main()
