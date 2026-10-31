import pygame as py

from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class info_text:
    """Draw the current round and short-lived shot result messages."""

    WHITE = (90, 75, 65)
    LIVE_COLOR = (220, 55, 45)
    BLANK_COLOR = (210, 190, 135)

    def __init__(self, screen):
        self.screen = screen
        self.round_font = py.font.Font(ASSETS_DIR / "fonts" / "Pixeltype.ttf", 54)
        self.result_font = py.font.Font(ASSETS_DIR / "fonts" / "Pixeltype.ttf", 48)
        self.current_round = 1
        self.shot_result = None
        self.result_until = 0
        self.result_starts = 0
        self.result_surface = None
        self.result_rect = None
        self.result_duration = 0

    def set_round(self, round_number):
        """Set the round number displayed at the top center of the screen."""
        self.current_round = round_number

    def show_shot_result(self, result, duration=2000, delay=1000):
        """Show the shot result after a delay, then fade it away."""
        if result is None:
            self.clear_shot_result()
            return

        normalized = str(result).strip().lower()
        if normalized not in ("live", "blank"):
            raise ValueError("result must be 'live', 'blank', or None")

        self.shot_result = normalized
        label = "IT WAS A LIVE ROUND" if normalized == "live" else "IT WAS A BLANK"
        color = self.LIVE_COLOR if normalized == "live" else self.BLANK_COLOR
        self.result_surface = self.result_font.render(label, True, color)
        self.result_rect = self.result_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 160)
        )
        self.result_duration = max(0, duration)
        self.result_starts = py.time.get_ticks() + max(0, delay)
        self.result_until = self.result_starts + self.result_duration

    def clear_shot_result(self):
        self.shot_result = None
        self.result_surface = None
        self.result_rect = None
        self.result_duration = 0
        self.result_starts = 0

    def update(self, round_number=None):
        """Update the round label and expire old shot result text."""
        if round_number is not None:
            self.set_round(round_number)

        if self.shot_result is not None and py.time.get_ticks() >= self.result_until:
            self.clear_shot_result()


    def draw(self):
        """Draw the round label and any active shot result."""
        round_surface = self.round_font.render(
            f"ROUND {self.current_round}", True, self.WHITE
        )
        round_rect = round_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(round_surface, round_rect)

        now = py.time.get_ticks()
        if self.result_surface is not None and now >= self.result_starts:
            remaining = max(0, self.result_until - now)
            fade_duration = min(500, self.result_duration)
            alpha = 255
            if fade_duration and remaining < fade_duration:
                alpha = int(255 * remaining / fade_duration)

            message = self.result_surface.copy()
            message.set_alpha(alpha)
            backing = self.result_rect.inflate(18, 10)
            box = py.Surface(backing.size, py.SRCALPHA)
            py.draw.rect(box, (15, 12, 12, int(220 * alpha / 255)), box.get_rect(), border_radius=6)
            self.screen.blit(box, backing)
            self.screen.blit(message, self.result_rect)

