import pygame.mixer
import game_config

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.volume = 0.5  # Default volume
        self.background_music = pygame.mixer.Sound('../my_pet/assets/rock_sound_effects/Game_Background_music.mp3')
    
    def load_track(self, track_path):
        self.current_track = track_path
        pygame.mixer.music.load(self.current_track)
    
    def play(self, loop=False):
        pygame.mixer.music.play(-1 if loop else 0)
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def unpause(self):
        pygame.mixer.music.unpause()
    
    def stop(self):
        pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)
    
    def quit(self):
        pygame.mixer.quit()

# How to use this class:
# music_player = MusicPlayer()
# music_player.load_track('path_to_your_music_file.mp3')
# music_player.play(loop=True)
