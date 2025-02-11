import json
import random

from src.game_state_management import GameState
from src.sprite_engine.tiles import Tile
from src.sprite_engine.player import Bat
from src.utils.sound_utils import change_background_music

class LevelManager:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

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
        self.bat_dims = level_json.get("bat_dims", (0.09, 0.025))

    def initialize_random_powers(self):
        """We have several powers that will be assigned to random matrix cells. Not implemented yet.
        Will implement it once i get the game physics going."""
        self.powers = []
        for x in range(self.num_powers):
            random_x = random.randrange(0, self.num_rows)
            random_y = random.randrange(0, self.num_cols)
            self.powers.append((random_x, random_y))

    def load_tiles(self):
        start_x = self.game_state.screen_width * self.tile_offsets['x']
        start_y = self.game_state.screen_height * self.tile_offsets['y']
        w = self.tile_width * self.game_state.screen_width
        h = self.tile_height * self.game_state.screen_height
        curr_x, curr_y = start_x, start_y
        for idx, row in enumerate(self.matrix):
            for idx2, cell in enumerate(row):
                coords = (curr_x, curr_y, w, h)
                is_double_hit = (idx, idx2) in self.double_hit_tiles
                tile = Tile(cell, coords, self.game_state, is_double_hit)
                self.game_state.tiles_group.add(tile)
                curr_x += w
            curr_x = start_x
            curr_y += h

    def load_bat(self):
        bat_x = self.bat_placement[0] * self.game_state.screen_width
        bat_y = self.bat_placement[1] * self.game_state.screen_height
        w = self.bat_dims[0] * self.game_state.screen_width
        h = self.bat_dims[1] * self.game_state.screen_height
        bat = Bat((bat_x, bat_y, w, h), self.game_state)
        self.game_state.bat_sprite = bat

    def load_level(self):
        level_json = self.load_json()
        self.build_level_json(level_json)
        change_background_music(self.background_music, 
                                game_state=self.game_state)
        self.game_state.screen_uis['game'].containers[0].set_background_image(self.background_image)
        self.load_tiles()
        self.load_bat()