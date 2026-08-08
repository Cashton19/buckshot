import pygame as py
from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, FPS 
from buckshot.scenes.player import Player
from buckshot.scenes.enemy import Enemy

class GameEnvironment:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(self.screen)
        self.enemy = Enemy(self.screen)
        self.bg_images = [
    py.transform.scale(
        py.image.load(ASSETS_DIR / "backgrounds" / f"{i}.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    for i in range(1, 6)
]
        self.bg_width = self.bg_images[0].get_width()
        self.scroll = 0
        self.speeds = [0.2, 0.4, 0.6, 0.8, 0]

    def update(self):
            self.scroll += 2
            
    def draw(self):
        

        for layer, image in enumerate(self.bg_images):
            offset = (self.scroll * self.speeds[layer]) % self.bg_width

            for x in range(-1, 2):
                self.screen.blit(
                    image,
                    (x * self.bg_width - offset, 0)
                )
    def run(self):
        clock = py.time.Clock()
        running = True

        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False

            self.update()

            self.screen.fill((0, 0, 0))
            self.draw()
            self.player.update()
            self.player.draw()
            self.enemy.update()
            self.enemy.draw()
            py.display.flip()
            clock.tick(FPS)

        py.quit()

    