import os

TILES_PATH = "assets/tiles/tile_sprites/"
LEVELS_PATH = "assets/levels/"

def map_files_list(path):
    item_dict = {}
    all_items = os.listdir(path)
    for item in all_items:
        item = item.replace(".png","")
        item_dict[item] = path + item
    return item_dict

TILES_DICT = map_files_list(TILES_PATH)
LEVELS_DICT = map_files_list(LEVELS_PATH)



