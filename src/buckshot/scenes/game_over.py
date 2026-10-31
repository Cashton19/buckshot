import pygame as py

from buckshot.config import ASSETS_DIR


class GameOver:
    """Draw a victory overlay announcing the winning player."""

    GOLD = (235, 185, 75)
    PALE_GOLD = (255, 226, 153)
    DARK = (25, 19, 22)
    MUTED = (191, 174, 151)

    def __init__(self, screen, winner, player1=None, player2=None):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.started_at = py.time.get_ticks()
        self.fade_duration = 450

        self.title_font = py.font.Font(
            ASSETS_DIR / "fonts" / "Pixeltype.ttf", max(40, int(self.height * 0.09))
        )
        self.winner_font = py.font.Font(
            ASSETS_DIR / "fonts" / "Pixeltype.ttf", max(56, int(self.height * 0.12))
        )
        self.detail_font = py.font.Font(
            ASSETS_DIR / "fonts" / "Pixeltype.ttf", max(25, int(self.height * 0.045))
        )
        self.winner_label = self._winner_name(winner, player1, player2)

    @staticmethod
    def _winner_name(winner, player1, player2):
        if isinstance(winner, str):
            return winner.upper()
        if player1 is not None and winner is player1:
            return "PLAYER 1"
        if player2 is not None and winner is player2:
            return "PLAYER 2"
        return str(getattr(winner, "name", "WINNER")).upper()

    def update(self):
        """Advance the overlay's short fade-in."""
        elapsed = py.time.get_ticks() - self.started_at
        self.alpha = min(255, int(255 * elapsed / self.fade_duration))

    def draw(self):
        """Draw the victory panel over the current game screen."""
        alpha = getattr(self, "alpha", 0)
        overlay = py.Surface((self.width, self.height), py.SRCALPHA)
        overlay.fill((8, 7, 10, int(205 * alpha / 255)))
        self.screen.blit(overlay, (0, 0))

        panel_width = int(self.width * 0.62)
        panel_height = int(self.height * 0.48)
        panel = py.Rect(0, 0, panel_width, panel_height)
        panel.center = (self.width // 2, self.height // 2)

        panel_surface = py.Surface(panel.size, py.SRCALPHA)
        py.draw.rect(
            panel_surface,
            (*self.DARK, int(245 * alpha / 255)),
            panel_surface.get_rect(),
            border_radius=22,
        )
        self.screen.blit(panel_surface, panel)

        border = py.Surface(panel.size, py.SRCALPHA)
        py.draw.rect(
            border,
            (*self.GOLD, alpha),
            border.get_rect(),
            width=3,
            border_radius=22,
        )
        self.screen.blit(border, panel)

        accent_y = panel.top + int(panel.height * 0.12)
        py.draw.line(
            self.screen,
            (*self.GOLD, alpha),
            (panel.left + int(panel.width * 0.16), accent_y),
            (panel.right - int(panel.width * 0.16), accent_y),
            2,
        )

        self._draw_text("MATCH COMPLETE", self.detail_font, self.MUTED,
                        (self.width // 2, panel.top + int(panel.height * 0.25)), alpha)
        self._draw_text(f"{self.winner_label} WINS", self.winner_font, self.PALE_GOLD,
                        (self.width // 2, panel.centery), alpha)
        self._draw_text("VICTORY", self.title_font, self.GOLD,
                        (self.width // 2, panel.bottom - int(panel.height * 0.22)), alpha)

    def _draw_text(self, text, font, color, center, alpha):
        surface = font.render(text, True, color)
        surface.set_alpha(alpha)
        self.screen.blit(surface, surface.get_rect(center=center))
