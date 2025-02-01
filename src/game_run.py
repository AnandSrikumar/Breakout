import pygame

from src.event_management import EventHandler
from src.game_state_management import GameState
from src.ui.ui_build import build_ui, draw_ui

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
        

    def event_loop(self):
        """Iterates the events and calls handle_events method"""
        for event in pygame.event.get():
            self._event_handler.handle_events(event)
    
    def game_loop(self):
        """The main game loop."""
        while self._game_state.running:
            self.event_loop()
            self._screen.fill((0, 0, 0))
            draw_ui(game_state=self._game_state)
            pygame.display.flip()
    pygame.quit()

