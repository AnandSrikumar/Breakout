import pygame

from src.game_state_management import GameState

"""Module to manage sounds. We load all kind of sounds here."""

class SoundManager:
    def __init__(self):
        pygame.mixer.pre_init()
        self.sounds = {}
        sound_path = "assets/sounds/"
        self.__load_sound(f"{sound_path}option_select.wav", "button_hover", 100)
        self.background_music = "background_menu"

    def __load_sound(self, filepath: str,
                    name: str,
                    cool_down: float=0,
                    volume: float=1.0):
        """Private method that will load the sound from filepath and then updates the self.sounds dict with
        sound, lastplayed and cool_down. We do that to keep some delay in playing a particular sound."""
        sound = pygame.mixer.Sound(filepath)
        sound.set_volume(volume) 
        self.sounds[name] = {"sound": sound, 
                             "last_played": 0, 
                             "cool_down": cool_down}
        
    def play_sound(self, name: str):
        """This is for playing sounds, not background music. We check if thhe sound is available in the dict and
        it has been at least cool_down period since it was last played."""
        if name not in self.sounds:
            return
        sound = self.sounds[name]['sound']
        last_played = self.sounds[name]['last_played']
        cool_down = self.sounds[name]['cool_down']
        current_time = pygame.time.get_ticks()
        if current_time - last_played > cool_down:
            sound.play()
            self.sounds[name]['last_played'] = current_time

    def play_music(self, loop=True, start_time=49):
        """Plays background music using pygame.mixer.music"""
        music_path = f"assets/sounds/{self.background_music}"
        if "." not in self.background_music:
            music_path = f"assets/sounds/{self.background_music}.mp3"
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1 if loop else 0, start_time)
        except pygame.error as e:
            print(f"[ERROR] Failed to load background music: {e}")

    def stop_music(self):
        """Stops the background music."""
        pygame.mixer.music.stop()

        
    
