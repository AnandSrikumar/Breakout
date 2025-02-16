import pygame

from src.game_state_management import GameState
from src.game_configs import POWERS, POWER_FALL_SPEED, BALL_SPEED
from src.log_handle import get_logger
from src.sprite_engine.ball import Ball

logger = get_logger(__name__)

class PowerHandler:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.orig_bat_size = self.game_state.bat_sprite.rect.w

    def __make_fire_balls(self):
        for ball in self.game_state.ball_sprite_group:
            ball.is_fireball = True

    def __change_ball_velocity(self, vel):
        for ball in self.game_state.ball_sprite_group:
            ball.velocity.speed = BALL_SPEED * vel

    def __create_multi_balls(self):
        new_balls = []
        for ball in self.game_state.ball_sprite_group:
            coords = (ball.rect.x, ball.rect.y, ball.rect.w / 2, ball.rect.h / 2)
            b1 = Ball(coords, self.game_state)
            b2 = Ball(coords, self.game_state)
            b1.velocity.x = -BALL_SPEED * 0.8
            b2.velocity.x = BALL_SPEED * 0.8
            b1.is_sticky = False
            b2.is_sticky = False
            new_balls.extend([b1, b2])
        for ball in new_balls:
            self.game_state.ball_sprite_group.add(ball)
        
    def assign_power(self, power_name):
        match power_name:
            case "big_bat":
                self.game_state.bat_sprite.make_bat_big()
            case "small_bat":
                self.game_state.bat_sprite.make_bat_small()
            case "bullets_bat":
                self.game_state.bat_sprite.change_bat('bullets')
            case "magnet_bat":
                self.game_state.bat_sprite.change_bat("magnet")
            case "fire_ball":
                self.__make_fire_balls()
            case "fast_ball":
                self.__change_ball_velocity(1.9)
            case "slow_ball":
                self.__change_ball_velocity(0.5)
            case "multi_ball":
                self.__create_multi_balls()


class Power(pygame.sprite.Sprite):
    def __init__(self,
                 game_state: GameState,
                 coords: tuple,
                 power_name: str):
        super().__init__()
        self.game_state = game_state
        self.coords = coords
        self.power_name = power_name
        self.image_path = POWERS[power_name]
        self.power_handle = PowerHandler(game_state)
        self.load_frames()

    def load_frames(self):
        image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(image, (self.coords[2], self.coords[3]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.coords[0], self.coords[1])
    
    def collide_check(self):
        if not (self.rect.colliderect(self.game_state.bat_sprite.rect)):
            return
        self.power_handle.assign_power(self.power_name)
        self.game_state.sound_manager.play_sound("power_gain")
        self.kill()

    def update(self, dt):
        self.collide_check()
        self.rect.y += POWER_FALL_SPEED * dt
        if self.rect.y >= self.game_state.screen_height:
            self.kill()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

