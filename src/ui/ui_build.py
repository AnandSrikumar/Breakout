import json
import os

from pygame import Surface, image, transform

from src.game_state_management import GameState
from src.log_handle import get_logger
from src.ui.containers import rectangle_builder

logger = get_logger(__name__)

"""Module to build screen. Tried to keep this object as generic as possible, it can be used to build all the screens in the UI
We use json to create the UI, the json has tree structure. Check assets/screens/ and check some json files to know better.
We use all the coords as offset %ages like 0.5 means 50%
There are few gui elements
1. Parents: we call them containers. I defined 2 types of containers, I might define more.
    1. Rectangle container
    2. circle container
    containers act as outer most elements, the coords are directly related to the main screen. ex: if the xcoord of 
    the container is 0.5 then it is placed at 50% location of the screen horizontally.

2. children: We call them buttons, texts, userinputs. We have 2 buttons
    1. RectangleButton
    2. Circle button
    Buttons act as inner elements, their coords are calculated w.r.t to the container they are in. If button x coord is
    0.5 then we calculate the container (x,y,width, height) and then we do button_x =x + (width * 0.5)

I tried to keep the UI design as simple as possible yet became very complicated
,  I predefined how my UIs would look like.

"""


class ScreenUI:
    def __init__(self, game_state: GameState):
        self._game_state = game_state
        self._screen = self._game_state.screen

    def set_screen_name(self, screen_name: str):
        self.screen_name = screen_name
        return self

    def set_backgroud_image(self, background_image: str):
        if background_image:
            bg_image = image.load(background_image)
            bg_image = transform.scale(
                bg_image,
                (self._game_state.screen_width, self._game_state.screen_height),
            )
            self.background_image = bg_image
            return self
        self.background_image = None
        return self

    def set_contents(self, contents: list[dict]):
        self.containers = []
        for content in contents:
            match content:
                case {"RectangleContainer": value}:
                    self.containers.append(rectangle_builder(value, self._game_state))

                case {"CircleContainer": value}:
                    ...
                case _:
                    logger.error(
                        f"Error! Invalid container: {str(list(content.keys())[0])}"
                    )
                    raise ValueError("Invalid container detected in configuration...")


def parse_jsons() -> dict:
    """
    Iterates all the jsons in /assets/screens and returns the list of dictionaries (we read json as dictionary)
    """
    path = "assets/screens/"
    screens = os.listdir(path)
    all_screens = []
    for screen in screens:
        if not screen.endswith(".json"):
            continue
        with open(f"{path}{screen}") as fp:
            screen_json = json.load(fp)
            all_screens.append(screen_json)
    return all_screens


def build_ui(game_state: GameState):
    """We build the UI objects. We build individual components for the UI and add them in ui_components list
    UI_components list will be set up as instance variable of game_state object."""
    all_screens = parse_jsons()
    screens = {}
    for screen in all_screens:
        screen_obj = ScreenUI(game_state)
        screen_obj.set_screen_name(screen.get("screen_name")).set_backgroud_image(
            screen.get("background_image")
        ).set_screen_name(screen.get("screen_name")).set_contents(
            screen.get("contents")
        )
        screens[screen.get("screen_name")] = screen_obj
    game_state.screen_uis = screens
    game_state.current_screen = screens["main_menu"]


def handle_buttons(buttons):
    """This is to handle button hover, clicks and draw"""
    for button in buttons:
        button.draw()


def draw_ui(game_state: GameState):
    """Draws the screen containers and buttons, it will only draw current screen"""
    curr_screen = game_state.current_screen
    for container in curr_screen.containers:
        container.draw(game_state)
        handle_buttons(container.elements)
