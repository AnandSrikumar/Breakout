import pygame

from src.game_state_management import GameState

"""Module created to handle events more efficiently. To keep the code clean, the event handling
is delegated to a different module and a class. We harness match/case for better readability and pattern matching."""


class EventHandler:
    def __init__(self, game_state: GameState):
        """game_state is an object that has all the global variables"""
        self._game_state = game_state

    def quit_event(self, _):
        """Sets running to false, the loop gets exited and pygame quits."""
        self._game_state.running = False

    def key_down(self, event):
        """Handles key down events"""
        match event.key:
            case pygame.K_q:
                self._game_state.running = False

    def key_up(self, event):
        """Handles key up events"""
        ...

    def mouse_down(self):
        """Handles mouse down events"""
        ...

    def mouse_up(self):
        """Handles mouse up events"""
        ...

    def custom_event(self):
        """Handle custom events. These events are needed because we have to run some tasks with some delay
        and don't want to block the main loop. Custom events are very useful to perform some operation every few seconds.
        ex:
        CUSTOM_EVENT = pygame.USEREVENT + 1  # Create a unique event ID
        pygame.time.set_timer(CUSTOM_EVENT, 2000)

        The above custom event runs every 2 seconds, we can perform some task when that happens.
        This method is very complicated compared to all the other event handling methods.
        """
        ...

    def handle_events(self, event: pygame.event) -> bool:
        """takes event and Uses match/case to call the method that handles the specific event."""
        match event.type:
            case pygame.quit:
                self.quit_event(event)
                return True
            case pygame.KEYDOWN:
                self.key_down(event)
                return True
        return False
