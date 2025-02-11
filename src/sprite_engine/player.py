import pygame

from src.game_state_management import GameState
from src.game_configs import NORMAL_BAT, MAGNET_BAT, BULLETS_BAT
from src.log_handle import get_logger

logger = get_logger(__name__)

class Bat(pygame.sprite.Sprite):
    def __init__(self, 
                 coords: tuple,
                 game_state: GameState):
        self.coords = coords
        self.game_state = game_state
        self.is_bullets_available = False
        self.curr_frame = 0
        self.frame_change_delay = 50
        self.load_frames()
        self.current_time = pygame.time.get_ticks()

    def __load_transform(self, bats: list[str]):
        images = []
        for bat in bats:
            image = pygame.image.load(bat)
            image = pygame.transform.scale(image, (self.coords[2], self.coords[3]))
            images.append(image)
        return images

    def load_frames(self):
        self.normal_bats = self.__load_transform(NORMAL_BAT)
        self.magnet_bats = self.__load_transform(MAGNET_BAT)
        self.bullet_bats = self.__load_transform(BULLETS_BAT)
        self.current_bats_list = self.normal_bats
        self.image = self.normal_bats[self.curr_frame]
        self.curr_frames_len = len(self.normal_bats)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.coords[0], self.coords[1])

    def change_frame_check(self):
        current_time = pygame.time.get_ticks()
        if not ((current_time - self.current_time) >= self.frame_change_delay):
            return
        next_frame = self.curr_frame + 1
        if next_frame >= self.curr_frames_len:
            next_frame = 0
        self.curr_frame = next_frame
        self.image = self.current_bats_list[self.curr_frame]
        self.current_time = current_time

    def update(self, dt: float):
        self.change_frame_check()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
