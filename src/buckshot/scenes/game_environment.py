import pygame as py

from buckshot.config import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class GameEnvironment:

    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.result = None 
        self.stop_anims_event = py.USEREVENT + 1

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


        

    def handle_event(self, event):
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:                                
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
                
            elif event.key == py.K_s:
                # Shoot self
                self.result = self.game_state.shoot(self.game_state.turn_manager.current_player)
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
        
        
        
       
            