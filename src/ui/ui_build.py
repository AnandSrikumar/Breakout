import json
import os

from pygame import image, transform, Surface

from game_state_management import GameState
#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
#https://AnandSrikumar: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@github.com/AnandSrikumar/Breakout.git
class ScreenUI:
    def __init__(self, 
                 game_state: GameState,
                 screen: Surface):
        self._game_state = game_state
        self._screen = screen
    
    def parse_screen_name(self, screen_name: str):
        self.screen_name = screen_name
        return self
    
    def parse_backgroud_image(self, background_image: str):
        if background_image:
            bg_image = image.load(background_image)
            bg_image = transform.scale(bg_image, 
                                       (self._game_state.screen_width, 
                                        self._game_state.screen_height))
            self.background_image = bg_image
            return self
        self.background_image = None
        return self
    
    def parse_contents(self, contents: list[dict]):
        ...


def parse_jsons() -> dict:
    path = "/assets/screens/"
    screens = os.listdir("path")
    all_screens = []
    for screen in screens:
        if not screen.endswith(".json"):
            continue
        with open(f"{path}{screen}") as fp:
            screen_json = json.load(fp)
            all_screens.append(screen_json)
    return all_screens

def build_ui(game_state: GameState):
    all_screens = parse_jsons()