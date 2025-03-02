from typing import Any

import pygame

from src.game_state_management import GameState
from src.ui.elements import build_group
from src.utils import draw_utils

"""The module dedicated to build containers. Containers are sections within a screen. 
Containers can be of Rectangle and circle. They can be placed anywhere on the screen. We calculate their locations with offsets
ex: if container's x is 0.5 then its x is located at 50% of the screen.

Ooops, I mislabelled margin as padding.
"""


class BaseContainer:
    """A base class that sets backgroud_color, x and y coords"""

    def set_background_color(self, color: tuple | None):
        self.background_color = (0, 0, 0) if not color else color
        return self

    def set_x_coords(self, x_offset: float, screen_width: float):
        self.x_coordinate = screen_width * x_offset
        return self

    def set_y_coords(self, y_offset: float, screen_height: float):
        self.y_coordinate = screen_height * y_offset
        return self


class CircleContainer(BaseContainer):
    def set_background_image(self, img: str | None):
        img = draw_utils.set_circle_background(img, self.radius)
        self.background_image = img

    def set_size(self, radius_offset: float, screen_width: float):
        self.radius = screen_width * radius_offset
        return self

    def set_paddings(self, paddings: dict[str, float]):
        if not paddings:
            return self
        self.x_coordinate += paddings.get("left", 0) - paddings.get("right", 0)
        self.y_coordinate += paddings.get("up", 0) - paddings.get("down", 0)
        return self

    def set_groups(self, groups: list[dict], game_state: GameState): ...

    def draw(self, game_state: GameState):
        screen = game_state.screen
        pygame.draw.circle(
            screen,
            self.background_color,
            (self.x_coordinate, self.y_coordinate),
            self.radius,
        )
        if self.background_image:
            screen.blit(
                self.background_image, (self.x - self.radius, self.y - self.radius)
            )


class RectangleContainer(BaseContainer):
    def set_background_image(self, img: str | None):
        if not img:
            self.background_image = None
            return self
        background_image = draw_utils.set_rect_background(img, self.width, self.height)
        self.background_image = background_image
        return self

    def set_size(
        self,
        width_offset: float,
        height_offset: float,
        screen_width: float,
        screen_height: float,
    ):
        self.width = screen_width * width_offset
        self.height = screen_height * height_offset
        return self

    def set_paddings(self, paddings: dict[str, float]):
        if not paddings:
            return self
        left = paddings.get("left", 0)
        right = paddings.get("right", 0)
        up = paddings.get("up", 0)
        down = paddings.get("down", 0)
        self.x_coordinate += left
        self.width -= left + right
        self.y_coordinate += up
        self.height -= up + down
        return self

    def set_groups(self, groups: list[dict], game_state: GameState):
        self.elements = []
        for group in groups:
            group["x_coord"] = self.x_coordinate + (self.width * group["x_offset"])
            group["y_coord"] = self.y_coordinate + (self.height * group["y_offset"])
            group["x_gap_val"] = self.width * group["x_gap"]
            group["y_gap_val"] = self.height * group["y_gap"]
            group["container_dims"] = {
                "type": "rect",
                "width": self.width,
                "height": self.height,
            }
            self.elements.extend(build_group(group, game_state))

    def draw(self, game_state: GameState):
        screen = game_state.screen
        pygame.draw.rect(
            screen,
            self.background_color,
            (self.x_coordinate, self.y_coordinate, self.width, self.height),
        )
        if self.background_image:
            screen.blit(self.background_image, (self.x_coordinate, self.y_coordinate))


def rectangle_builder(container: dict[str, Any], game_state: GameState):
    rect_obj = RectangleContainer()
    rect_obj.set_background_color(container.get("background_color")).set_x_coords(
        container.get("x_offset"), game_state.screen_width
    ).set_y_coords(container.get("y_offset"), game_state.screen_height).set_size(
        container.get("width_offset"),
        container.get("height_offset"),
        game_state.screen_width,
        game_state.screen_height,
    ).set_paddings(
        container.get("padding", {})
    ).set_background_image(
        container.get("background_image")
    ).set_groups(
        container.get("groups", []), game_state
    )
    return rect_obj
