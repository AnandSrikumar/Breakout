from typing import Any
import pygame
from src.game_configs import TILES_DICT
from src.game_state_management import GameState
from src.sprite_engine.powers import Power

class Tile(pygame.sprite.Sprite):
    def __init__(self, 
                 image_name: str,
                 coords: tuple,
                 game_state: GameState,
                 is_double_hit: bool=False,
                 power: Any=None
                 ):
        super().__init__()
        self.image_path = TILES_DICT[image_name]
        self.image_name = image_name
        self.coords = coords
        self.is_broken = False
        self.hits_to_break = 1 if not is_double_hit else 2
        self.power = power
        self.game_state = game_state
        self.load_frames()

    def load_frames(self):
        """Loads sprites for the tiles, loads both normal tile and broken tile."""
        def load_transform(path, broken=False):
            """We create the sprite here."""
            if broken:
                path += "_broken"
            path += ".png"
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, 
                                            (self.coords[2], self.coords[3]))
            return image
        
        self.normal_frame = load_transform(self.image_path)
        self.broken_frame = load_transform(self.image_path, True)
        self.image = self.normal_frame
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.coords[0], self.coords[1])

    def update(self):
        if self.hits_to_break >= 1:
            return
        if self.power:
            coords = (self.rect.x, self.rect.y, self.rect.w * 0.6, self.rect.h * 0.6)
            power_sprite = Power(self.game_state, coords, self.power)
            self.game_state.powers_group.add(power_sprite)
        self.kill()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        
        