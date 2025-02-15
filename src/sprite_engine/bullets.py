import pygame
from src.game_state_management import GameState
from src.game_configs import BULLETS, BULLET_SPEED


class Bullet(pygame.sprite.Sprite):
    def __init__(self,
                 game_state: GameState,
                 coords: tuple):
        super().__init__()
        self.game_state = game_state
        self.coords = coords
        self.image = pygame.image.load(BULLETS).convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (coords[2], coords[3]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0], coords[1])
    
    def check_tile_collision(self):
        br_col = pygame.sprite.spritecollide(self, self.game_state.tiles_group, dokill=False)
        if br_col:
            br = br_col[0]
            br.hits_to_break -= 1
            self.kill()
    
    def check_out_of_bounds(self):
        if self.rect.y <= self.game_state.screen_height * 0.05:
            self.kill()

    def update(self, dt):
        self.rect.y -= BULLET_SPEED * dt
        self.check_tile_collision()
        self.check_out_of_bounds()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

def bullet_factory(game_state: GameState, coords: tuple):
    game_state.bullets_group.add(Bullet(game_state, coords))