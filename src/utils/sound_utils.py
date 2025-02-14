from src.game_state_management import GameState


def change_background_music(music: str, game_state: GameState, start_time=0, volume=0.5):
    game_state.sound_manager.stop_music()
    game_state.sound_manager.background_music = music
    game_state.sound_manager.play_music(start_time=start_time, volume=volume)