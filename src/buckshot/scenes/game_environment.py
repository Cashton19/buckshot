import pygame as py

from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class GameEnvironment:

    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.result = None 
        self.stop_anims_event = py.USEREVENT + 1
        self.action_button_font = py.font.Font(ASSETS_DIR / "fonts" / "Pixeltype.ttf", 16)
        self.action_button_color = (218, 166, 32)
        self.action_button_hover_color = (245, 195, 55)
        self.shoot_self_rect = py.Rect(0, 0, 190, 52)
        self.shoot_self_rect.center = (int(SCREEN_WIDTH * 0.38), SCREEN_HEIGHT - 42)
        self.shoot_opponent_rect = py.Rect(0, 0, 190, 52)
        self.shoot_opponent_rect.center = (int(SCREEN_WIDTH * 0.62), SCREEN_HEIGHT - 42)

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
        
        self.game_state.player1.play_idle_anims()
        self.game_state.player2.play_idle_anims()        

        # Align each player's feet with the ground line in background layer 7.
        ground_image = self.bg_images[-1]
        center_x = ground_image.get_width() // 2
        ground_y = next(
            (
                y for y in range(ground_image.get_height())
                if max(ground_image.get_at((center_x, y))[:3]) < 200
            ),
            int(ground_image.get_height() * 0.78),
        )
        self.game_state.player1.y = (
            ground_y - self.game_state.player1.total_frames[0].get_height()
        )
        self.game_state.player2.y = (
            ground_y - self.game_state.player2.total_frames[0].get_height()
        )


        

    def handle_event(self, event):
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            if self.shoot_opponent_rect.collidepoint(event.pos):                                
                if self.game_state.player1.is_animating: 
                    return

                if self.game_state.player2.is_animating:
                    return
                
                # Shoot opponent
                self.result = self.game_state.shoot(self.game_state.turn_manager.opponent)
                if self.result == "live" and self.game_state.turn_manager.current_player_index == 1:                   
                    self.game_state.player1.play_shoot_anims()
                    self.game_state.player2.play_hurt_anims()
                    py.time.set_timer(self.stop_anims_event, 1000, loops=1)
                    

                if self.result == "live" and self.game_state.turn_manager.current_player_index == 0:
                    self.game_state.player2.play_shoot_anims()
                    self.game_state.player1.play_hurt_anims()
                    py.time.set_timer(self.stop_anims_event, 1000, loops=1)
                 
                # self.game_state.info_text.set_round(self.game_state.round_manager.current_round)
                
                # self.game_state.info_text.clear_shot_result()
                print(f"Shot opponent! Result: {self.result}")
                print(self.game_state.shotgun.shells)
                print(self.game_state.round_manager.current_round)
                
            elif self.shoot_self_rect.collidepoint(event.pos):
                if self.game_state.player1.is_animating: 
                    return
    
                if self.game_state.player2.is_animating:
                    return
                # Shoot self
                self.result = self.game_state.shoot(self.game_state.turn_manager.current_player)
                if self.result == "live" and self.game_state.turn_manager.current_player_index == 0:
                    self.game_state.player1.play_hurt_anims()
                    py.time.set_timer(self.stop_anims_event, 1000, loops=1)
                if self.result == "live" and self.game_state.turn_manager.current_player_index == 1:
                    self.game_state.player2.play_hurt_anims()
                    py.time.set_timer(self.stop_anims_event, 1000, loops=1)
                # self.game_state.info_text.set_round(self.game_state.round_manager.current_round)
                self.game_state.info_text.show_shot_result(self.result)
                # self.game_state.info_text.clear_shot_result()
                print(f"Shot self! Result: {self.result}")
                print(self.game_state.round_manager.current_round)
            
            if self.game_state.game_over:
                print(f"Game Over! Winner: {self.game_state.winner}")
            self.game_state.info_text.show_shot_result(self.result)

        if event.type == self.stop_anims_event and self.game_state.turn_manager.current_player_index == 1 and self.result == "live":
            self.game_state.player1.stop_anims() 
            self.game_state.player2.stop_anims() 
            self.game_state.player1.play_idle_anims()
            self.game_state.player2.play_idle_anims()

        if event.type == self.stop_anims_event and self.game_state.turn_manager.current_player_index == 0 and self.result == "live":
            self.game_state.player2.stop_anims() 
            self.game_state.player1.stop_anims() 
            self.game_state.player2.play_idle_anims()
            self.game_state.player1.play_idle_anims()

    def update(self):
        self.scroll += 2
        self.game_state.info_text.update(self.game_state.round_manager.current_round)
        self.game_state.player_text.update()
        self.game_state.player_text.highlight(self.game_state.turn_manager.current_player_index)
        self.game_state.player1.update()
        self.game_state.player2.update()



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
        
        self.game_state.player1.draw()
        self.game_state.player2.draw()
        self.game_state.info_text.draw()
        self.game_state.player_text.draw()

        # Player 1 health bar (Left)
        p1_ratio = self.game_state.player1.health / self.game_state.player1.max_health
        self.game_state.p1_health_bar.draw(p1_ratio)

        # Player 2 health bar (Right)
        p2_ratio = self.game_state.player2.health / self.game_state.player2.max_health
        self.game_state.p2_health_bar.draw(p2_ratio)

        mouse_pos = py.mouse.get_pos()
        self._draw_action_button(self.shoot_self_rect, "Shoot Self", mouse_pos)
        self._draw_action_button(self.shoot_opponent_rect, "Shoot Opponent", mouse_pos)

    def _draw_action_button(self, rect, label, mouse_pos):
        """Draw a gold action button with a hover highlight."""
        color = (self.action_button_hover_color
                 if rect.collidepoint(mouse_pos) else self.action_button_color)
        py.draw.rect(self.screen, color, rect, border_radius=8)
        py.draw.rect(self.screen, (95, 67, 20), rect, width=3, border_radius=8)
        text = self.action_button_font.render(label, True, (35, 28, 18))
        self.screen.blit(text, text.get_rect(center=rect.center))
        
        
        
       
            
