import pygame

from buckshot.config import ASSETS_DIR


class Button:
    HOVER_LIFT = 8

    def __init__(self, text, image, center, size):
        self.text = text
        self.image = pygame.transform.smoothscale(image, size)
        self.rect = self.image.get_rect(center=center)

    def is_hovered(self, mouse_position):
        return self.rect.collidepoint(mouse_position)

    def draw(self, screen, mouse_position):
        hovered = self.is_hovered(mouse_position)
        draw_rect = self.rect.move(0, -self.HOVER_LIFT if hovered else 0)

        if hovered:
            shadow = pygame.Surface(draw_rect.size, pygame.SRCALPHA)
            pygame.draw.ellipse(
                shadow,
                (0, 0, 0, 80),
                (draw_rect.width * 0.12, draw_rect.height * 0.72,
                 draw_rect.width * 0.76, draw_rect.height * 0.22),
            )
            screen.blit(shadow, (draw_rect.x, draw_rect.bottom - 8))

        screen.blit(self.image, draw_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class MainMenu:
    def __init__(self, screen, title="BuckShot"):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.title = title
        self.background_color = (18, 15, 20)
        self.title_color = (244, 211, 135)
        self.subtitle_color = (191, 174, 151)
        self.toast_color = (241, 208, 126)

        self.title_font = pygame.font.Font(
            ASSETS_DIR / "fonts" / "Pixeltype.ttf", max(54, int(self.height * 0.11))
        )
        self.subtitle_font = pygame.font.Font(
            ASSETS_DIR / "fonts" / "Pixeltype.ttf", max(24, int(self.height * 0.045))
        )
        self.toast_font = pygame.font.Font(
            ASSETS_DIR / "fonts" / "Pixeltype.ttf", max(26, int(self.height * 0.05))
        )

        menu_assets = ASSETS_DIR / "ui" / "main_menu"
        button_specs = (
            ("Online", "online.png"),
            ("Two Players", "two_player.png"),
            ("Bot", "bot.png"),
            ("Options", "options.png"),
            ("Exit", "exit.png"),
        )

        target_height = self.height * 0.135
        buttons = []
        for index, (label, filename) in enumerate(button_specs):
            source = pygame.image.load(menu_assets / filename).convert_alpha()
            source_rect = source.get_bounding_rect(min_alpha=1)
            image = source.subsurface(source_rect).copy()

            scale = min(
                target_height / image.get_height(),
                (self.width * 0.55) / image.get_width(),
            )
            size = (
                max(1, int(image.get_width() * scale)),
                max(1, int(image.get_height() * scale)),
            )
            center = (
                self.width // 2,
                int(self.height * (0.27 + index * 0.135)),
            )
            buttons.append(Button(label, image, center, size))

        self.buttons = buttons
        self.toast_message = None
        self.toast_until = 0

    def draw(self):
        self.screen.fill(self.background_color)

        title_surface = self.title_font.render(self.title, True, self.title_color)
        self.screen.blit(
            title_surface,
            title_surface.get_rect(center=(self.width // 2, int(self.height * 0.075))),
        )

        subtitle_surface = self.subtitle_font.render(
            "CHOOSE YOUR GAME MODE", True, self.subtitle_color
        )
        self.screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(center=(self.width // 2, int(self.height * 0.15))),
        )

        mouse_position = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_position)

        if self.toast_message:
            toast_surface = self.toast_font.render(
                self.toast_message, True, self.toast_color
            )
            toast_rect = toast_surface.get_rect(
                center=(self.width // 2, int(self.height * 0.94))
            )
            backing = toast_rect.inflate(32, 18)
            pygame.draw.rect(
                self.screen, (28, 23, 27), backing, border_radius=10
            )
            pygame.draw.rect(
                self.screen, (151, 110, 43), backing, width=2, border_radius=10
            )
            self.screen.blit(toast_surface, toast_rect)

        pygame.display.flip()

    def update(self):
        if self.toast_message and pygame.time.get_ticks() >= self.toast_until:
            self.toast_message = None

    def handle_event(self, event):
        for button in self.buttons:
            if not button.clicked(event):
                continue

            if button.text == "Two Players":
                return "play"
            if button.text == "Exit":
                return "quit"

            self.toast_message = "COMING SOON"
            self.toast_until = pygame.time.get_ticks() + 1800

        return None
