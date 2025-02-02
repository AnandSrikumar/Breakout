import pygame

from abc import ABC, abstractmethod

from src.game_state_management import GameState

class Button(ABC):
    def __init__(
                    self,
                    coords: tuple,
                    text: str,
                    text_weight: str,
                    text_size: int,
                    font: str|None,
                    text_color: tuple,
                    hover: tuple,
                    background_color: tuple,
                    game_state: GameState
                 ):
        self.coords = coords
        self.text = text
        self.text_weight = text_weight
        self.text_size = text_size
        self.font = pygame.font.Font(font, text_size)
        self.font.set_bold(text_weight=="bold")
        self.hover = hover
        self.background_color = background_color
        self.game_state = game_state
        self.screen = self.game_state.screen
        self.text_color = text_color
        self.coords_rect = pygame.Rect(*self.coords)

    @abstractmethod
    def draw(self):
        ...

class RectangleButton(Button):
    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, self.coords, 0)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.coords_rect.center)
        self.game_state.screen.blit(text_surface, text_rect)

class CircleButton(Button):
    def draw(self):
        pygame.draw.circle(self.screen, 
                           self.background_color, 
                           self.coords[0:2],
                           self.coords[2])
        
def build_group(group: dict, game_state: GameState):
    elements = group.get('elements', [])
    elements_objects = []
    for element in elements:
        match element:
            case {"RectangleButton": value}:
                container_dims = group['container_dims']
                if container_dims['type'] == 'rect':
                    coords = (group['x_coord'],
                              group['y_coord'],
                              container_dims['width'] * value['width_offset'],
                              container_dims['height'] * value['height_offset'])
                elif container_dims['type'] == 'circle':
                    coords = (group['x_coord'],
                              group['y_coord'],
                              container_dims['radius'] * 2 * value['width_offset'],
                              container_dims['radius'] * 2 * value['height_offset'])
                obj = RectangleButton(coords, value['text'],
                                      group['text_weight'],
                                      group['text_size'],
                                      group['font'],
                                      group.get("text_color", (255, 255, 255)),
                                      group.get('hover',group['background_color']),
                                      group['background_color'],
                                      game_state)
                elements_objects.append(obj)
        group['x_coord'] = group['x_coord'] + group['x_gap_val']
        group['y_coord'] = group['y_coord'] + group['y_gap_val']
    return elements_objects