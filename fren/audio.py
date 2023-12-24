import os
import logging
logger = logging.getLogger()

import pygame
from fren import helpers

class SoundMaster:
    """
        https://pixabay.com/music/search/game%20intro/?pagi=3
    """

    def __init__(self):
        # self.quiet = App.get_instance().manifest.get("quiet", False)
        # pygame.mixer.music.set_volume(1)

        # self.dink_effect = pygame.mixer.Sound( os.path.join(helpers.HERE, 'resources', 'bling.mp3') )
        self.dink_effect = pygame.mixer.Sound( helpers.get_resource("bling.mp3") )
        self.dink_effect.set_volume(1)

        # self.lemmethink_effect = pygame.mixer.Sound( os.path.join(helpers.HERE, 'resources', "lemmethink.mp3" ) )
        self.lemmethink_effect = pygame.mixer.Sound( helpers.get_resource("lemmethink.mp3") )
        self.lemmethink_effect.set_volume(1)

    def dink(self):
        self.dink_effect.play()

    def lemmethink(self):
        self.lemmethink_effect.play()


_audio = None

def audio() -> SoundMaster:
    global _audio
    if _audio is None:
        _audio = SoundMaster()
    return _audio

# _audio = audio()
