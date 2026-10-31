import pygame as py

from buckshot.config import ASSETS_DIR


class TinyBullet:
    """Display remaining shell icons for the current round."""

    def __init__(self, screen, bullet_height=28, spacing=6):
        self.screen = screen
        self.spacing = spacing

        source = py.image.load(ASSETS_DIR / "ui" / "bullet.png").convert_alpha()
        visible_area = source.get_bounding_rect(min_alpha=1)
        source = source.subsurface(visible_area).copy()

        bullet_width = round(source.get_width() * bullet_height / source.get_height())
        self.bullet_image = py.transform.smoothscale(
            source, (bullet_width, bullet_height)
        )
        self.bullets = []

    def append_bullet(self, total_bullets):
        """Set the displayed bullet count for a new round."""
        if total_bullets < 0:
            raise ValueError("total_bullets cannot be negative")
        self.bullets = [self.bullet_image] * total_bullets

    def remove_bullet(self):
        """Remove one displayed bullet after a shot, if any remain."""
        if self.bullets:
            self.bullets.pop()

    def update(self, total_bullets=None):
        """Optionally synchronize the icons with the current shell count."""
        if total_bullets is not None and len(self.bullets) != total_bullets:
            self.append_bullet(total_bullets)

    def draw(self):
        """Draw the remaining bullet icons in a centered row."""
        if not self.bullets:
            return

        bullet_width = self.bullet_image.get_width()
        total_width = len(self.bullets) * bullet_width + (len(self.bullets) - 1) * self.spacing
        screen_width, screen_height = self.screen.get_size()
        start_x = (screen_width - total_width) // 2
        y = int(screen_height * 0.20 - self.bullet_image.get_height() / 2)

        for index, bullet in enumerate(self.bullets):
            x = start_x + index * (bullet_width + self.spacing)
            self.screen.blit(bullet, (x, y))
