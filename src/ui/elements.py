from abc import ABC, abstractmethod
from typing import Any

import pygame

from src.game_state_management import GameState
from src.utils import draw_utils
from src.log_handle import get_logger

logger = get_logger(__name__)

"""This module is dedicated for creating buttons and other elements.
Elements are componenets within container. the location of elements is w.r.t to the container not the screen."""


class Button(ABC):
    """Abstract class for buttons, has all the required configs to create the button and place a text at center"""

    def __init__(
        self,
        coords: tuple,
        text: str,
        text_weight: str,
        text_size: int,
        font: str | None,
        text_color: tuple,
        hover: tuple,
        background_color: tuple,
        background_image: str|None,
        game_state: GameState,
    ):
        self.coords = coords
        self.text = text
        self.text_weight = text_weight
        self.text_size = text_size
        self.font = pygame.font.Font(font, text_size)
        self.font.set_bold(text_weight == "bold")
        self.hover = hover
        self.background_color = background_color
        self.original_color = background_color
        self.game_state = game_state
        self.screen = self.game_state.screen
        self.text_color = text_color
        self.coords_rect = pygame.Rect(*self.coords) if len(self.coords) == 4 else None
        self.background_image = background_image
        self.background_image_obj = None

    @abstractmethod
    def draw_background_image(self):
        ...
            
    @abstractmethod
    def draw(self): ...


class RectangleButton(Button):
    """Rectangle implementation of the button."""
    def draw_background_image(self):
        if self.background_image is None:
            return
        return draw_utils.set_rect_background(self.background_image,
                                                                   self.coords_rect.w,
                                                                   self.coords_rect.h)

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, self.coords, 0)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.coords_rect.center)
        self.screen.blit(text_surface, text_rect)
        if not self.background_image_obj:
            self.background_image_obj = self.draw_background_image()
        else:
            self.screen.blit(self.background_image_obj, self.coords_rect)


class CircleButton(Button):
    """Circle implementation of button"""
    def draw_background_image(self):
        if self.background_image is None:
            return
        return draw_utils.set_circle_background(self.background_image,
                                                                   self.coords_rect.w,
                                                                   self.coords_rect.h)
    
    def draw(self):
        """Draw implementation for circle"""


def rectangle_build(group: dict, 
                    value: dict, 
                    game_state: GameState
                    ) -> RectangleButton:
    """Function to build rectangle"""
    container_dims = group["container_dims"]
    if container_dims["type"] == "rect":
        coords = (
            group["x_coord"],
            group["y_coord"],
            container_dims["width"] * value["width_offset"],
            container_dims["height"] * value["height_offset"],
        )
    elif container_dims["type"] == "circle":
        coords = (
            group["x_coord"],
            group["y_coord"],
            container_dims["radius"] * 2 * value["width_offset"],
            container_dims["radius"] * 2 * value["height_offset"],
        )
    obj = RectangleButton(
        coords,
        value["text"],
        group["text_weight"],
        group["text_size"],
        group["font"],
        group.get("text_color", (255, 255, 255)),
        group.get("hover", group["background_color"]),
        group["background_color"],
        value.get("background_image"),
        game_state,
    )
    return obj

def circle_build(group: dict, 
                 value: dict, 
                 game_state: GameState) -> CircleButton:
    """Builds circle object"""
    container_dims = group["container_dims"]
    if container_dims["type"] == "rect":
         coords = (
            group["x_coord"],
            group["y_coord"],
            container_dims["width"] * value["radius"],
        )
    elif container_dims["type"] == "circle":
        ...
    
    return CircleButton(
        coords,
        value.get("text"),
        group["text_weight"],
        group["text_size"],
        group["font"],
        group.get("text_color", (255, 255, 255)),
        group.get("hover", group.get("background_color", (0, 0, 0))),
        group.get("background_color", (0, 0, 0)),
        value.get("background_image"),
        game_state,
    )

def build_group(group: dict, game_state: GameState) -> list[Any]:
    """
    This function is called by container class, the group parameter is group key from the json. Container class adds
    some key: values to the group before calling this function, container class will calculate the button class x and y coords
    it will also add the type of container to the group. The container class adds group['container_dims'], container dims will
    have buttons' x and y coords and container's width and height, in this function, we calculate the button's width and height
    and creat the button object as per its type. We currently have RectangleButton and CircleButton. Remember. Groups key
    will have all the common configs, the groups key will have elements key, elements key contains buttons. only
    text, width_offset and height_offset are inside elements key, rest are under the groups only. elements is a list of dicts.
    """
    elements = group.get("elements", [])
    elements_objects = []
    for element in elements:
        match element:
            case {"RectangleButton": value}:
                obj = rectangle_build(group, value, game_state)
            case {"CircleButton": value}:
                obj = circle_build(group, value, game_state)

        elements_objects.append(obj)
        group["x_coord"] = group["x_coord"] + group["x_gap_val"]
        group["y_coord"] = group["y_coord"] + group["y_gap_val"]
    return elements_objects
