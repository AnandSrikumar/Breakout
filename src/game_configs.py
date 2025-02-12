import os

TILES_PATH = "assets/tiles/tile_sprites/"
LEVELS_PATH = "assets/levels/"
BALL_PATH = "assets/Ball.png"

def map_files_list(path):
    item_dict = {}
    all_items = os.listdir(path)
    for item in all_items:
        item = item.replace(".png","")
        item_dict[item] = path + item
    return item_dict

TILES_DICT = map_files_list(TILES_PATH)
LEVELS_DICT = map_files_list(LEVELS_PATH)

BULLETS_BAT = ["assets/tiles/bats/bullets.png", 
               'assets/tiles/bats/bullets2.png',
               "assets/tiles/bats/bullets3.png"]

MAGNET_BAT = ["assets/tiles/bats/magnet.png"]
NORMAL_BAT = ["assets/tiles/bats/normal1.png",
              "assets/tiles/bats/normal2.png",
              "assets/tiles/bats/normal3.png"]

BAT_MOVEMENT_SPEED = 550

