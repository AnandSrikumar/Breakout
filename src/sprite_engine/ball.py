import math
import pygame

from src.game_state_management import GameState
from src.game_configs import BALL_PATH, BALL_SPEED, MAX_ANGLE
from src.log_handle import get_logger

logger = get_logger(__name__)

class Velocity:
    def __init__(self, x: int, 
                 y: int, 
                 speed: int=BALL_SPEED, 
                 max_angle: int=MAX_ANGLE):
        self.x = x
        self.y = y
        self.speed = speed
        self.max_angle = max_angle

    def angle_modify(self, hit_pos: float):
        bounce_angle = hit_pos * self.max_angle
        self.x = BALL_SPEED * math.sin(bounce_angle)
        self.y = -BALL_SPEED * math.cos(bounce_angle)


class Ball(pygame.sprite.Sprite):
    def __init__(self,
                 coords: tuple,
                 game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.coords = coords
        self.is_fireball = False
        self.is_sticky = True
        self.current_time = pygame.time.get_ticks()
        self.sticky_time = 2000
        self.velocity = Velocity(BALL_SPEED * 0.6, -BALL_SPEED)
        self.sw = self.game_state.screen_width
        self.sh = self.game_state.screen_height
        self.load_frame()
        
    def load_frame(self):
        dims = (self.coords[2] * 2, self.coords[2] * 2)
        BALL_RADIUS = self.coords[2]
        image = pygame.image.load(BALL_PATH).convert_alpha()
        image = pygame.transform.smoothscale(image, dims)
        mask_surface = pygame.Surface(dims, pygame.SRCALPHA)
        pygame.draw.circle(mask_surface, (255, 255, 255, 255), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS) 
        image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.rect = image.get_rect(center=(self.coords[0], self.coords[1]))
        self.prev_rect = self.rect.copy()
        self.image = image

    def modify_sticky(self):
        if not self.is_sticky:
            return
        current_time = pygame.time.get_ticks()
        if self.is_sticky and current_time - self.current_time > self.sticky_time:
            logger.info("Made sticky false")
            self.is_sticky = False

    def sticky_movement(self, bat_coords):
        self.rect.x = bat_coords[0] + bat_coords[2] // 2
        self.rect.y = bat_coords[1] - self.rect.h

    def bounds_check(self):
        if (self.rect.x <= self.sw * 0.01) or (self.rect.x >= self.sw * 0.98):
            self.velocity.x *= -1
        if (self.rect.y <= self.sh * 0.05):
            self.velocity.y *= -1
    
    def paddle_collision_check(self):
        bat_rect = self.game_state.bat_sprite.rect
        if (not self.rect.colliderect(bat_rect)) or \
                (self.rect.y >= self.game_state.screen_height):
            return
        hit_pos = (self.rect.centerx - bat_rect.centerx) / (bat_rect.w / 2)
        self.velocity.angle_modify(hit_pos=hit_pos)
    
    def tiles_collision(self):
        collided_bricks = pygame.sprite.spritecollide(self, self.game_state.tiles_group, dokill=False)
        if not collided_bricks:
            return  
        brick = collided_bricks[0]
        brick.hits_to_break -= 1
        self.game_state.sound_manager.play_sound("brick_hit")
        if self.prev_rect.right <= brick.rect.left:
            self.velocity.x *= -1
        elif self.prev_rect.left >= brick.rect.right:
            self.velocity.x *= -1
        elif self.prev_rect.bottom <= brick.rect.top:
            self.velocity.y *= -1
        elif self.prev_rect.top >= brick.rect.bottom:
            self.velocity.y *= -1

    def wall_collision(self):
        if self.rect.colliderect(self.game_state.walls['left']) or \
                self.rect.colliderect(self.game_state.walls['right']):
            self.velocity.x *= -1
            return
        if self.rect.colliderect(self.game_state.walls['top']):
            self.velocity.y *= -1

    def move_ball(self, dt):
        bat = self.game_state.bat_sprite
        bat_x, bat_y = bat.rect.x, bat.rect.y
        bat_w, bat_h = bat.rect.w, bat.rect.h
        if self.is_sticky:
            self.sticky_movement((bat_x, bat_y, bat_w, bat_h))
            return
        self.prev_rect = self.rect.copy()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def key_bindings(self):
        if self.game_state.space_pressed:
            self.is_sticky = False
    
    def check_ball_dead(self):
        if self.rect.y >= self.game_state.screen_height:
            self.kill()

    def debug_draw(self):
        pygame.draw.rect(self.game_state.screen,
                         (255, 0, 0), self.rect, 1)

    def update(self, dt: float|int):
        self.modify_sticky()
        self.move_ball(dt)
        self.bounds_check()
        self.paddle_collision_check()
        self.key_bindings()
        self.tiles_collision()
        self.check_ball_dead()
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)