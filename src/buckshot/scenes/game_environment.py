import pygame as py

from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class GameEnvironment:

    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.result = None

    # redering background
        self.bg_images = [
            py.transform.scale(
                py.image.load(
                    ASSETS_DIR / "backgrounds" / f"{i}.png"
                ).convert_alpha(),
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            for i in range(1, 8)
        ]
        self.bg_width = self.bg_images[0].get_width()
        self.scroll = 0
        self.speeds = [
            0,
            1,
            0.8,
            0.6,
            0.4,
            0.2,
            0
        ]
        
    # Rendering health bar
        health_bar_width = int(SCREEN_WIDTH * 0.38)
        
        original_health_bar = py.image.load(
            ASSETS_DIR / "ui" / "health_bar" / "health_bar.png"
        ).convert_alpha()

        original_depleted = py.image.load(
            ASSETS_DIR / "ui" / "health_bar" / "health_bar_depleted.png"
        ).convert_alpha()

        # Preserve aspect ratio
        health_bar_height = int(
            original_health_bar.get_height()
            * (health_bar_width / original_health_bar.get_width())
        )

        self.health_bar = py.transform.smoothscale(
            original_health_bar,
            (health_bar_width, health_bar_height)
        )

        self.health_bar_depleted = py.transform.smoothscale(
            original_depleted,
            (health_bar_width, health_bar_height)
        )

        # Position: top-left with responsive margin
        self.margin_x = int(SCREEN_WIDTH * 0.05)
        self.top_padding = int(SCREEN_HEIGHT * 0.03)
        player_text_space = int(SCREEN_HEIGHT * 0.08)
        health_bar_y = player_text_space + 10


        self.health_bar_rect = self.health_bar.get_rect(
            topleft=(self.margin_x, health_bar_y)
        )
        
        self.health_bar_right_rect = self.health_bar.get_rect(
            topright=(
                SCREEN_WIDTH - self.margin_x + 10,
                health_bar_y
            )            
        )
        
        # render text
        self.font = py.font.Font(ASSETS_DIR / "fonts" / "Pixeltype.ttf", 32)
        self.player_name_left = self.font.render("Player 1", True, (255, 255, 255))
        self.player_name_right = self.font.render("Player 2", True, (255, 255, 255))
        
        
            


    def handle_event(self, event):
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                # Shoot opponent
                self.result = self.game_state.shoot(self.game_state.turn_manager.opponent)
                if self.result == "live" and self.game_state.turn_manager.current_player_index == 0:
                    self.game_state.player1.idle =  py.image.load(ASSETS_DIR / "sprites" / "character1" / "shoot.png").convert_alpha()
                    print("animation played")
                
                print(f"Shot opponent! Result: {self.result}")
            elif event.key == py.K_s:
                # Shoot self
                self.result = self.game_state.shoot(self.game_state.turn_manager.current_player)
                print(f"Shot self! Result: {self.result}")
            
            if self.game_state.game_over:
                print(f"Game Over! Winner: {self.game_state.winner}")

    def update(self):
        self.scroll += 2
        if self.game_state.turn_manager.current_player_index == 0:
            self.player_name_left = self.font.render("Player 1", True, (255, 0, 0))
            self.player_name_right = self.font.render("Player 2", True, (255, 255, 255))
        elif self.game_state.turn_manager.current_player_index == 1:
            self.player_name_left = self.font.render("Player 1", True, (255, 255, 255))
            self.player_name_right = self.font.render("Player 2", True, (255, 0, 0))
            
        self.player_name_left_rect = self.player_name_left.get_rect(
            topleft=(self.margin_x, self.top_padding)
        )
        self.player_name_right_rect = self.player_name_right.get_rect(
            topright=(
                SCREEN_WIDTH - self.margin_x,
                self.top_padding
                )  
        )



    def draw(self):
        # background
        self.screen.fill((0, 0, 0))
        for layer, image in enumerate(self.bg_images):
            offset = (
                self.scroll * self.speeds[layer]
            ) % self.bg_width
            for x in range(-1, 2):
                self.screen.blit(
                    image,
                    (
                        x * self.bg_width - offset,
                        0
                    )
                )
        
        # Player 1 health bar (Left)
        p1_ratio = self.game_state.player1.health / self.game_state.player1.max_health
        p1_width = int(self.health_bar_rect.width * p1_ratio)
        
        self.screen.blit(self.health_bar_depleted, self.health_bar_rect)
        self.screen.blit(
            self.health_bar, 
            self.health_bar_rect, 
            (0, 0, p1_width, self.health_bar_rect.height)
        )

        # Player 2 health bar (Right)
        p2_ratio = self.game_state.player2.health / self.game_state.player2.max_health
        p2_width = int(self.health_bar_right_rect.width * p2_ratio)
        
        self.screen.blit(self.health_bar_depleted, self.health_bar_right_rect)
        self.screen.blit(
            self.health_bar, 
            self.health_bar_right_rect, 
            (0, 0, p2_width, self.health_bar_right_rect.height)
        )
        
        self.screen.blit(self.player_name_left, self.player_name_left_rect)
        self.screen.blit(self.player_name_right, self.player_name_right_rect)
            