import random


class Shotgun:
    """Manages the shells contained inside the shotgun."""

    LIVE = "live"
    BLANK = "blank"

    def __init__(self, live_shells: int, blank_shells: int):
        if live_shells < 0 or blank_shells < 0:
            raise ValueError("Shell counts cannot be negative.")

        if live_shells + blank_shells == 0:
            raise ValueError("Shotgun must contain at least one shell.")

        self.max_live_shells = live_shells
        self.max_blank_shells = blank_shells

        self.shells = []
        self.live_count = 0
        self.blank_count = 0

        self._generate_shells()
        self.shuffle()

    def _generate_shells(self):
        """Generate the initial live and blank shells."""
        self.shells = (
            [self.LIVE] * self.max_live_shells
            + [self.BLANK] * self.max_blank_shells
        )

        self.live_count = self.max_live_shells
        self.blank_count = self.max_blank_shells

    def shuffle(self):
        """Randomize the order of the remaining shells."""
        random.shuffle(self.shells)

    def fire(self) -> str:
        """
        Fire the next shell.

        Returns:
            str: Either Shotgun.LIVE or Shotgun.BLANK.

        Raises:
            RuntimeError: If there are no shells remaining.
        """
        if self.is_empty():
            raise RuntimeError("The shotgun is empty.")

        shell = self.shells.pop(0)

        if shell == self.LIVE:
            self.live_count -= 1
        else:
            self.blank_count -= 1

        return shell

    def is_empty(self) -> bool:
        """Return True if there are no shells remaining."""
        return len(self.shells) == 0

    def remaining(self) -> int:
        """Return the total number of shells remaining."""
        return len(self.shells)

    def has_live_shells(self) -> bool:
        """Return True if at least one live shell remains."""
        return self.live_count > 0

    def has_blank_shells(self) -> bool:
        """Return True if at least one blank shell remains."""
        return self.blank_count > 0