import pygame

from src.game_state_management import GameState
from src.game_configs import POWERS, POWER_FALL_SPEED, BALL_SPEED
from src.log_handle import get_logger

logger = get_logger(__name__)

class PowerHandler:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.orig_bat_size = self.game_state.bat_sprite.rect.w

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
        self.kill()

    def update(self, dt):
        self.collide_check()
        self.rect.y += POWER_FALL_SPEED * dt
        if self.rect.y >= self.game_state.screen_height:
            self.kill()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

