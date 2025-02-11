from typing import Any
from src.game_state_management import GameState
from src.ui.elements import Button
from src.log_handle import get_logger
from src.level_handler import LevelManager

logger = get_logger(__name__)

"""Module dedicated to handle UI button presses and hovers."""

class MainMenu():
    """class to handle main menu UI handling"""
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.current_focus = 0
        self.button_pressed = False
        self.mouse_pos = game_state.mouse_pos
    
    def __inc_index(self):
        """When down is pressed, we move the focus to the next button, so that next button changes its background color"""
        if self.current_focus >= self.button_len -1:
            self.current_focus = 0
            return
        self.current_focus += 1

    def __dec_index(self):
        """When up is pressed, we move the focus to prev button"""
        if self.current_focus == 0:
            self.current_focus = self.button_len - 1
            return
        self.current_focus -= 1

    def __mouse_hover_check(self, button, idx):
        """We assume the button is hovered if the mouse is not static it goes to the row of the button."""
        mouse_pos = self.game_state.mouse_pos
        if mouse_pos == self.mouse_pos:
            return
        _, mouse_y = mouse_pos
        if mouse_y >= button.coords[1] and \
                  mouse_y < button.coords[1] + button.coords[-1]:
                self.current_focus = idx
                # self.game_state.sound_manager.play_sound("button_hover")

    
    def __key_hover_check(self):
        """We handle up and down button presses, based on the up and down, we move the hover focus up and down.
        If current focus is out of bounds, we bring them to the bounds (if x>len(matrix) 
        then x=0, if x < 0 then x = len(matrix) -1)"""
        logger.info("Mouse unmoved. Checking key hover")
        if self.game_state.up_pressed:
            logger.info("Up button pressed")
            self.game_state.up_pressed = False
            self.__dec_index()
            self.game_state.sound_manager.play_sound("button_hover")
        elif self.game_state.down_pressed:
            logger.info("down button pressed")
            self.game_state.down_pressed = False
            self.__inc_index()
            self.game_state.sound_manager.play_sound("button_hover")

    def button_functionality(self, text: str):
        """We check the button text and handle the event accordingly"""
        if not (self.game_state.enter_pressed or self.game_state.mouse_down):
            return
        match text:
            case "EXIT":
                self.game_state.running = False
            case "PLAY":
                self.game_state.current_screen = "game"
                self.game_state.game_handle.load_game_screen()

    def handle_buttons(self, buttons: list[Button]):
        """We do everything with this method. We call hover check methods, button functionality method, etc"""
        self.button_len = len(buttons)
        for idx, button in enumerate(buttons):
            if idx == self.current_focus:
                button.background_color = button.hover
            else:
                button.background_color = button.original_color
            self.__mouse_hover_check(button, idx)
            self.__key_hover_check()
            button.draw()
            self.button_functionality(button)
        if self.current_focus >= self.button_len or self.current_focus < 0:
            return
        hover_text = buttons[self.current_focus].text
        self.button_functionality(hover_text)
    
    def handle_main_menu(self, buttons: list[Button]):
        self.handle_buttons(buttons)

class GameScreen:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def load_game_screen(self):
        self.level = LevelManager(game_state=self.game_state)
        self.level.load_level()

def initialize_ui_handles(game_state: GameState):
    """
    We might have multiple screens and each screen will have a class to handle the ui.
    We initialize objects for each one of the screen and store it in game state instance variable
    """
    game_state.main_menu_handle = MainMenu(game_state)
    game_state.game_handle = GameScreen(game_state)

def handle_ui(game_state: GameState, 
              container: Any, 
              screen_name:str) -> Any:
    """Game state has a current_screen object, that points to the screen that should be rendered. 
    We check the current screen and return the appropriate screen object"""
    match screen_name:
        case "main_menu":
            handler = game_state.main_menu_handle
            handler.handle_main_menu(container.elements)
            return
        case "game":
            handler = game_state.game_handle
            
def draw_ui(game_state: GameState):
    """Draws the screen containers and buttons, it will only draw current screen"""
    curr_screen_name = game_state.current_screen
    curr_screen = game_state.screen_uis[curr_screen_name]
    for container in curr_screen.containers:
        container.draw(game_state)
        handle_ui(game_state, container, curr_screen_name)
