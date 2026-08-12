class TurnManager:
    """Manages the turn order between two players."""

    def __init__(self, player1, player2, starting_player=0):
        self.players = [player1, player2]

        if starting_player not in (0, 1):
            raise ValueError("starting_player must be 0 or 1.")

        self.current_player_index = starting_player

    @property
    def current_player(self):
        """Return the player whose turn it currently is."""
        return self.players[self.current_player_index]

    @property
    def opponent(self):
        """Return the player whose turn it is not."""
        return self.players[1 - self.current_player_index]

    def switch_turn(self):
        """Switch the turn to the other player."""
        self.current_player_index = 1 - self.current_player_index

    def reset(self, starting_player=0):
        """Reset the turn manager to a specific starting player."""
        if starting_player not in (0, 1):
            raise ValueError("starting_player must be 0 or 1.")

        self.current_player_index = starting_player