import pygame


class SoundManager:
    """Manages all sounds for the game"""
    def __init__(self):

        # Initialize pygame mixer
        pygame.mixer.init(44100, 16, 2, 4096)
        pygame.mixer.set_num_channels(16)

        # Create channels
        self.channels = [pygame.mixer.Channel(i) for i in range(16)]

    def play_music(self, music):
        self.clear_all_music_channels_except(music['channel'])
        self.play_track(channel=music['channel'], sound=music['sound'], volume=music['vol'])

    def clear_all_music_channels_except(self, channel):
        for i, ch in enumerate(self.channels[:5]):
            if i != channel:
                ch.stop()

    def play_sound(self, fx):
        self.play_sound_fx(channel=fx['channel'], sound=fx['sound'], volume=fx['vol'])

    def play_track(self, channel, sound, volume):
        if not self.channels[channel].get_busy():
            self.channels[channel].set_volume(volume)
            self.channels[channel].play(sound, loops=-1)

    def play_sound_fx(self, channel, sound, volume):
        if not self.channels[channel].get_busy():
            self.channels[channel].set_volume(volume)
            self.channels[channel].play(sound)

    def stop_all_music(self):
        for channel in self.channels:
            channel.stop()
