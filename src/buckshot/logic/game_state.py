from buckshot.logic.shotgun import Shotgun
from buckshot.logic.turn_manager import TurnManager
from buckshot.scenes.player import Player


class GameState:
    """Owns and manages the state of a Buckshot game."""

    def __init__(
        self,
        screen,
        live_shells=3,
        blank_shells=3,
        player_health=5
    ):
        self.screen = screen

        # Shell configuration
        self.live_shells = live_shells
        self.blank_shells = blank_shells

        # Players
        self.player1 = Player(
            screen,
            x=-100,
            y=-180,
            flipped=False,
            health=player_health
        )

        self.player2 = Player(
            screen,
            x=700,
            y=-180,
            flipped=True,
            health=player_health
        )

        # Game systems
        self.shotgun = Shotgun(
            live_shells=self.live_shells,
            blank_shells=self.blank_shells
        )

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

        # 2. Fire the shotgun
        shell = self.shotgun.fire()

        # 3. Apply damage only for a live shell
        if shell == Shotgun.LIVE:
            target.take_damage()

            # 6. Check if the target is still alive
            if not target.is_alive():
                self.winner = current_player
                self.game_over = True
                return shell

        # 4. Shooting yourself with a blank keeps the turn
        if (
            target is current_player
            and shell == Shotgun.BLANK
        ):
            self._reload_if_empty()
            return shell

        # 5. Every other outcome switches the turn
        self.turn_manager.switch_turn()

        # 7. Reload if the shotgun is empty
        self._reload_if_empty()

        return shell

    def _reload_if_empty(self):
        """Create a new shotgun when the current one is empty."""

        if self.game_over:
            return

        if self.shotgun.is_empty():
            self.shotgun = Shotgun(
                live_shells=self.live_shells,
                blank_shells=self.blank_shells
            )

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