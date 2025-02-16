import json
import random
from pygame.rect import Rect

from src.game_state_management import GameState
from src.sprite_engine.tiles import Tile
from src.sprite_engine.player import Bat
from src.sprite_engine.ball import Ball
from src.utils.sound_utils import change_background_music
from src.game_configs import POWERS

class LevelManager:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.powers_list = list(POWERS.keys())

    def load_json(self):
        """Loads level json from assets/level. Make sure that level jsons file names follow this pattern
        levelx.json ex: level1.json, level2.json andso on. Because we semi hardcoded the path hahahaha"""
        level = self.game_state.level
        path = f"assets/levels/level{level}.json"
        with open(path) as fp:
            level_json = json.load(fp)
        return level_json
    
    def build_level_json(self, level_json: dict):
        """Reading all the fields of the json, makes it little easy."""
        self.num_rows = level_json['num_rows']
        self.num_cols = level_json['num_cols']
        self.double_hit_tiles = level_json['double_hit_tiles']
        self.num_powers = level_json['num_powers']
        self.background_music = level_json['background_music']
        self.background_image = level_json['background_image']
        self.matrix = level_json['matrix']
        self.tile_offsets = level_json['tiles_offsets']
        self.tile_width = level_json['tiles_dims']['width']
        self.tile_height = level_json['tiles_dims']['height']
        self.bat_placement = level_json.get("bat_placement", (0.45, 0.93))
        self.ball_placement = level_json.get("ball_placement", (0.5, 0.92))
        self.bat_dims = level_json.get("bat_dims", (0.09, 0.025))
        self.ball_dims = level_json.get("ball_dims", (0.007, 0.007))

    def initialize_random_powers(self):
        """We have several powers that will be assigned to random matrix cells. Not implemented yet.
        Will implement it once i get the game physics going."""
        self.powers = []
        for x in range(self.num_powers):
            random_x = random.randrange(0, self.num_rows)
            random_y = random.randrange(0, self.num_cols)
            self.powers.append((random_x, random_y))

    def __load_power(self, idx1, idx2):
        if (idx1, idx2) in self.powers:
            return random.choice(self.powers_list)
        
    def load_tiles(self):
        start_x = self.game_state.screen_width * self.tile_offsets['x']
        start_y = self.game_state.screen_height * self.tile_offsets['y']
        w = self.tile_width * self.game_state.screen_width
        h = self.tile_height * self.game_state.screen_height
        curr_x, curr_y = start_x, start_y
        for idx, row in enumerate(self.matrix):
            for idx2, cell in enumerate(row):
                if cell:
                    power = self.__load_power(idx, idx2)
                    coords = (curr_x, curr_y, w, h)
                    is_double_hit = (idx, idx2) in self.double_hit_tiles
                    tile = Tile(cell, coords, self.game_state, is_double_hit, power)
                    self.game_state.tiles_group.add(tile)
                curr_x += w + w*0.08
            curr_x = start_x
            curr_y += h + h*0.08

    def __load_player(self, placement, dims):
        x = placement[0] * self.game_state.screen_width
        y = placement[1] * self.game_state.screen_height
        w = dims[0] * self.game_state.screen_width
        h = dims[1] * self.game_state.screen_height
        return (x, y, w, h)

    def load_bat(self):
        coords = self.__load_player(self.bat_placement, self.bat_dims)
        bat = Bat(coords, self.game_state)
        self.game_state.bat_sprite = bat
    
    def load_ball(self):
        coords = self.__load_player(self.ball_placement, self.ball_dims)
        coords = (coords[0], coords[1], coords[2])
        ball = Ball(coords, self.game_state)
        self.game_state.ball_sprite_group.add(ball)

    def load_side_walls(self):
        self.game_state.walls['left'] = Rect(0, 0, 
             self.game_state.screen_width*0.02, 
             self.game_state.screen_height)
        
        self.game_state.walls['right'] = Rect(self.game_state.screen_width*0.98, 0, 
             self.game_state.screen_width*0.02, 
             self.game_state.screen_height)
        
        self.game_state.walls['top'] = Rect(0, 0, 
             self.game_state.screen_width, 
             self.game_state.screen_height*0.02)
        
    def reset_bat_ball(self):
        self.load_bat()
        self.load_ball()

    def load_level(self):
        level_json = self.load_json()
        self.build_level_json(level_json)
        change_background_music(self.background_music, 
                                game_state=self.game_state, volume=0.5)
        self.game_state.screen_uis['game'].containers[0].set_background_image(self.background_image)
        self.initialize_random_powers()
        self.load_tiles()
        self.load_bat()
        self.load_ball()
        self.load_side_walls()