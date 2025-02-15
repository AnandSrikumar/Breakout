import math
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

POWERS_PATH = "assets/tiles/powers/"
POWERS = {
    "big_bat": f"{POWERS_PATH}big_bat.png",
    "small_bat": f"{POWERS_PATH}small_bat.png",
    "bullets_bat": f"{POWERS_PATH}bullets_bat.png",
    "slow_ball": f"{POWERS_PATH}slow_ball.png",
    "fast_ball": f"{POWERS_PATH}fast_ball.png",
    "magnet_ball": f"{POWERS_PATH}magnet_ball.png",
    "fire_ball": f"{POWERS_PATH}fire_ball.png",
    "multi_ball": f"{POWERS_PATH}multi_ball.png"
}
POWER_FALL_SPEED = 310
BAT_MOVEMENT_SPEED = 660
BALL_SPEED = 12
MAX_ANGLE = math.radians(60)