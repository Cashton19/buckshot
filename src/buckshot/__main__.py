import pygame as py
import sys

from buckshot.config import FPS
from buckshot import BuckShot
from buckshot.scenes.main_menu import MainMenu
from buckshot.scenes.game_environment import GameEnvironment
from buckshot.scenes.game_over import GameOver
from buckshot.logic.game_state import GameState

py.init()
def main():   
    game = BuckShot()    
    menu = MainMenu(
        game.screen,
        title="BuckShot"
    )
    game_state = GameState(game.screen)  
    game_environment = GameEnvironment(
        game.screen,
        game_state,
    )  
    game_over_screen = None
    current_scene = "menu"
    while True:
        game.clock.tick(FPS)
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
                if game_state.game_over and game_over_screen is None:
                    game_over_screen = GameOver(
                        game.screen,
                        game_state.winner,
                        game_state.player1,
                        game_state.player2,
                    )

        if current_scene == "menu":
            menu.update()
        elif current_scene == "game":
            game_environment.update()
            game_state.update()

        if current_scene == "menu":
            menu.draw()
        elif current_scene == "game":
            game_environment.draw()
            game_state.draw()
            if game_over_screen is not None:
                game_over_screen.update()
                game_over_screen.draw()
            py.display.flip()
if __name__ == "__main__":
    main()
