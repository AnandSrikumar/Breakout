from typing import Any

from pygame import Surface
from pygame.sprite import Group

"""This module contains a class named GameState, this object is very useful because it maintains global variables.
We created this so that we need not to pass too many values to constructor of different objects.
all the objects will use important variables from this object."""


class GameState:
    """Maintains a global state"""

    def __init__(self):
        self.FPS: int = 60
        self.dt: int = 0
        self.running: bool = True
        self.sound_manager = None
        self._screen: Surface | None = None
        self.screen_uis: dict[Any] = {}
        self.current_screen: Any = None
        self.mouse_pos: tuple = None
        self.main_menu_handle: Any = None
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.mouse_down = False
        self.enter_pressed = False
        self.space_pressed = False
        self.tiles_group = Group()
        self.bat_sprite = None
        self.level = 1

    @property
    def screen(self) -> Surface:
        return self._screen

    @screen.setter
    def screen(self, screen: Surface) -> None:
        self.screen_width, self.screen_height = screen.get_size()
        self._screen = screen
