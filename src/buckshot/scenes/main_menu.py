import pygame
import sys


class Button:
    def __init__(self, text, center, size=(320, 60)):
        self.text = text
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center

        self.base_color = (58, 110, 165)
        self.hover_color = (91, 157, 255)
        self.text_color = (255, 255, 255)
        self.radius = 12

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()

        color = (
            self.hover_color
            if self.rect.collidepoint(mouse)
            else self.base_color
        )

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=self.radius
        )

        text_surface = font.render(
            self.text,
            True,
            self.text_color
        )

        screen.blit(
            text_surface,
            text_surface.get_rect(center=self.rect.center)
        )

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class MainMenu:

    def __init__(self, screen, title="GAME TITLE"):

        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.title = title

        self.bg_color = (15, 18, 35)

        self.title_font = pygame.font.SysFont(
            "arial",
            64,
            bold=True
        )

        self.button_font = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )

        button_texts = [
            "Online",
            "Two Players",
            "Bot",
            "Quit"
        ]

        start_y = 260
        spacing = 90

        self.buttons = []

        for i, text in enumerate(button_texts):

            button = Button(
                text,
                (
                    self.width // 2,
                    start_y + i * spacing
                )
            )

            self.buttons.append(button)

    def draw(self):

        self.screen.fill(self.bg_color)

        title_surface = self.title_font.render(
            self.title,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title_surface,
            title_surface.get_rect(
                center=(self.width // 2, 120)
            )
        )

        subtitle = pygame.font.SysFont(
            "arial",
            22
        ).render(
            "Select a Game Mode",
            True,
            (180, 180, 180)
        )

        self.screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(self.width // 2, 175)
            )
        )

        for button in self.buttons:
            button.draw(self.screen, self.button_font)

        pygame.display.flip()

    def run(self):

        clock = pygame.time.Clock()

        while True:

            clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for button in self.buttons:

                    if button.clicked(event):

                        if button.text in ("Two Players", "Bot"):
                            return "play"

                        elif button.text == "Quit":
                            pygame.quit()
                            sys.exit()

                        elif button.text == "Online":
                            return "online"

                        return button.text

            self.draw()