from buckshot.logic.shotgun import Shotgun
from buckshot.logic.turn_manager import TurnManager
from buckshot.logic.round_manager import RoundManager
from buckshot.scenes.player import Player
from buckshot.scenes.health_bar import health_bar
from buckshot.scenes.player_text import player_text
from buckshot.scenes.info_text import info_text
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class GameState:
    """Owns and manages the state of a Buckshot game."""

    def __init__(
        self,
        screen,
        live_shells=4,
        blank_shells=4,
        player_health=5
    ):
        self.screen = screen

        # Shell configuration
        self.live_shells = live_shells
        self.blank_shells = blank_shells

        # Players
        self.player_text = player_text(screen)     
        self.info_text = info_text(screen)   
        self.player1 = Player(
            screen,
            x= -(SCREEN_WIDTH * 0.08),
            y= -(SCREEN_HEIGHT * 0.22),
            flipped=False,
            health=player_health
        )
        self.player2 = Player(
            screen,
            x= SCREEN_WIDTH * 0.55,
            y=-(SCREEN_HEIGHT * 0.22),
            flipped=True,
            health=player_health
        )
        self.p1_health_bar = health_bar(screen)
        self.p2_health_bar = health_bar(screen, flipped = True)
        

        # Game systems
        self.shotgun = Shotgun(
            live_shells=self.live_shells,
            blank_shells=self.blank_shells  
            # first round with 50/50 chance of survival
        )
        
        self.round_manager = RoundManager()

        self.turn_manager = TurnManager(
            self.player1,
            self.player2
        )

        # Game state
        self.game_over = False
        self.winner = None

    def shoot(self, target):
        """
        Fire the shotgun at the given target.

        The target must be either the current player or their opponent.
        """

        # 1. Reject shots if the game is already over
        if self.game_over:
            return None

        current_player = self.turn_manager.current_player
        opponent = self.turn_manager.opponent

        # Validate target
        if target not in (current_player, opponent):
            raise ValueError("Invalid shooting target.")
        shell = self.shotgun.fire()

        # 3. Apply damage only for a live shell
        if shell == Shotgun.LIVE:
            target.take_damage()

            # 6. Check if the target is still alive
            if not target.is_alive():
                self.winner = current_player
                self.game_over = True
                return shell

        # 5. Every other outcome switches the turn
        self.turn_manager.switch_turn()

        # go to next round
        self.round_manager.next_round(self.turn_manager, self.shotgun)

        return shell


    def reset(self):
        """Reset the entire game."""

        self.player1.health = self.player1.max_health
        self.player2.health = self.player2.max_health

        self.shotgun = Shotgun(
            live_shells=self.live_shells,
            blank_shells=self.blank_shells
        )

        self.turn_manager.reset()

        self.game_over = False
        self.winner = None
        
    def update(self):
        """Update game objects."""

        # If your Player class has update()
        self.player1.update()
        self.player2.update()

    def draw(self):
        """Draw all game state objects."""

        self.player1.draw()
        self.player2.draw()