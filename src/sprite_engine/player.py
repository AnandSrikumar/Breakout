import pygame

from src.game_state_management import GameState
from src.game_configs import NORMAL_BAT, MAGNET_BAT, BULLETS_BAT, BAT_MOVEMENT_SPEED
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
        self.big_factor = 1.5
        self.small_factor = 0.6
        self.bat_frames = {"normal":{"big":[], "small": [], "normal": []},
                           "magnet":{"big":[], "small": [], "normal": []},
                           "bullets": {"big":[], "small": [], "normal": []}}
        self.load_frames()
        self.current_time = pygame.time.get_ticks()
        self.velocity_goal = 0
        self.bounds = (2, self.game_state.screen_width - 2)
        self.current_bat = "normal"
        self.can_shoot = False

    def __load_transform(self, bats: list[str], dims: tuple):
        images = []
        for bat in bats:
            image = pygame.image.load(bat).convert_alpha()
            image = pygame.transform.scale(image, dims)
            images.append(image)
        return images
    

    def __load_powered_bats(self, bats: list[str], bat_name):
        dims = [self.coords[2], self.coords[3]]
        small_dims = [self.coords[2] * self.small_factor, 
                      self.coords[3]]
        big_dims = [self.coords[2] * self.big_factor, 
                    self.coords[3]]

        normal = self.__load_transform(bats, dims)
        big = self.__load_transform(bats, big_dims)
        small = self.__load_transform(bats, small_dims)

        self.bat_frames[bat_name]['normal'] = normal
        self.bat_frames[bat_name]['small'] = small
        self.bat_frames[bat_name]['big'] = big


    def load_frames(self):
        self.__load_powered_bats(NORMAL_BAT, "normal")
        self.__load_powered_bats(MAGNET_BAT, "magnet")
        self.__load_powered_bats(BULLETS_BAT, "bullets")
        self.current_bat_list = self.bat_frames['normal']['normal']
        self.curr_frames_len = len(self.current_bat_list)
        self.image = self.current_bat_list[self.curr_frame]
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
        self.image = self.current_bat_list[self.curr_frame]
        self.current_time = current_time


    def key_bindings(self):
        if self.game_state.left_pressed and \
                    self.rect.x > self.bounds[0]:
            self.velocity_goal = -BAT_MOVEMENT_SPEED
        elif self.game_state.right_pressed and \
                    (self.rect.x + self.rect.w) < self.bounds[1]:
            self.velocity_goal = BAT_MOVEMENT_SPEED
        else:
            self.velocity_goal = 0


    def move_bat(self, dt: float):
        if dt > 0.15:
            dt = 0.15
        self.rect.x += self.velocity_goal * dt


    def update(self, dt: float):
        self.change_frame_check()
        self.key_bindings()
        self.move_bat(dt)


    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)



    def __modify_rect(self, frame):
        prev_x, prev_y = self.rect.x, self.rect.y
        self.rect = frame.get_rect()
        self.rect.topleft = (prev_x, prev_y)


    def __modify_bat(self, size):
        self.current_bat_list = self.bat_frames[self.current_bat][size]
        self.curr_frame = 0
        self.curr_frames_len = len(self.current_bat_list)
        self.__modify_rect(self.current_bat_list[self.curr_frame])
        

    def make_bat_big(self):
        self.__modify_bat('big')


    def make_bat_small(self):
        self.__modify_bat('small')

    
    def change_bat(self, bat_name):
        self.current_bat_list = self.bat_frames[bat_name]['normal']
        self.curr_frame = 0
        self.current_bat = bat_name
        self.__modify_rect(self.current_bat_list[self.curr_frame])
        