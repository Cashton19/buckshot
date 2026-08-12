import pygame as py
import sys

from buckshot.config import FPS
from buckshot import BuckShot
from buckshot.scenes.main_menu import MainMenu
from buckshot.scenes.game_environment import GameEnvironment
from buckshot.scenes.player import Player


def main():

    # Initialize game
    game = BuckShot()

    # Create scenes
    menu = MainMenu(
        game.screen,
        title="BuckShot"
    )

    game_environment = GameEnvironment(
        game.screen
    )

    player1 = Player(game.screen)
    player2 = Player(game.screen,-100 * -7, -180, True )

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

                elif selection == "online":
                    current_scene = "online"

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
            player1.update()
            player2.update()

        # -------------------------
        # Draw
        # -------------------------

        if current_scene == "menu":

            menu.draw()

        elif current_scene == "game":

            game_environment.draw()
            player1.draw()
            player2.draw()
            py.display.flip()
            

        elif current_scene == "online":

            game.screen.fill((0, 0, 0))
            py.display.flip()


if __name__ == "__main__":
    main()