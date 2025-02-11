import pygame

from src.event_management import EventHandler
from src.game_state_management import GameState
from src.ui.ui_build import build_ui
from src.ui.ui_handle import draw_ui, initialize_ui_handles
from src.sound_manager import SoundManager

"""
This module contains the class GameRunner, this class has the method that starts the game loop.
This is the entry point where pygame is initialized and all the required game objects are created.
The gameloop updates the state and runs 60 times a second.
"""


class GameRunner:
    def __init__(self):
        self._game_state = GameState()
        self._event_handler = EventHandler(self._game_state)
        pygame.init()
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Breakout")
        self._game_state.screen = self._screen
        build_ui(self._game_state)
        initialize_ui_handles(self._game_state)
        self._game_state.sound_manager = SoundManager()
        self._game_state.sound_manager.play_music()

    def event_loop(self):
        """Iterates the events and calls handle_events method"""
        for event in pygame.event.get():
            self._event_handler.handle_events(event)

    def calculate_mouse_pos(self):
        self._game_state.mouse_pos = pygame.mouse.get_pos()

    def update_sprite_groups(self):
        def update_and_draw(group, **kwargs):
            if group is None:
                return
            group.update(**kwargs)
            group.draw(self._screen)
        
        update_and_draw(self._game_state.tiles_group)
        update_and_draw(self._game_state.bat_sprite, dt=0)

    def game_loop(self):
        """The main game loop."""
        clock = pygame.time.Clock()
        while self._game_state.running:
            self.event_loop()
            self._screen.fill((0, 0, 0))
            self.calculate_mouse_pos()
            draw_ui(game_state=self._game_state)
            self.update_sprite_groups()
            pygame.display.flip()
            self._game_state.dt = clock.tick(self._game_state.FPS)

    pygame.quit()
