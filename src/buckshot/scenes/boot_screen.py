import math

import pygame as py

from buckshot.config import ASSETS_DIR


class BootScreen:
    """Show the game logo and wait for a key press to continue."""

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        background = py.image.load(ASSETS_DIR / "boot_screen.png").convert_alpha()
        self.background = py.transform.smoothscale(
            background, (self.width, self.height)
        )
        self.prompt_font = py.font.Font(
            ASSETS_DIR / "fonts" / "Pixeltype.ttf", max(30, int(self.height * 0.055))
        )
        self.prompt = self.prompt_font.render(
            "PRESS ANY KEY TO START GAME", True, (235, 205, 130)
        )

    def handle_event(self, event):
        """Return True when the player presses a key to continue."""
        return event.type == py.KEYDOWN

    def update(self):
        """Pulse the prompt gently to make it easy to notice."""
        pulse = (math.sin(py.time.get_ticks() / 450) + 1) / 2
        self.prompt.set_alpha(150 + int(105 * pulse))

    def draw(self):
        """Draw the stretched boot image and start prompt."""
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(
            self.prompt,
            self.prompt.get_rect(center=(self.width // 2, int(self.height * 0.78))),
        )
        py.display.flip()
