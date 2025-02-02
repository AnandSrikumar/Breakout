from typing import Any

from pygame import Surface

"""This module contains a class named GameState, this object is very useful because it maintains global variables.
We created this so that we need not to pass too many values to constructor of different objects.
all the objects will use important variables from this object."""


class GameState:
    """Maintains a global state"""

    def __init__(self):
        self.running: bool = True
        self._screen: Surface | None = None
        self.screens: dict[Any] = {}
        self.current_screen: Any = None

    @property
    def screen(self) -> Surface:
        return self._screen

    @screen.setter
    def screen(self, screen: Surface) -> None:
        self.screen_width, self.screen_height = screen.get_size()
        self._screen = screen
