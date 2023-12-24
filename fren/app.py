import os
import platform
import threading
import time

import dotenv
import pygame
from openai import OpenAI

from fren import helpers
from fren.logger import setup_logging
from fren.model.audiorecorder import AudioRecorder







from fren.model.singleton import Singleton
from fren.config import *

class App(Singleton):
    running: bool = None


    @classmethod
    def get_instance(cls) -> 'App':
        if cls._instance:
            return cls._instance
        else:
            return cls.configure_instance()

    @classmethod
    def configure_instance(cls) -> 'App':
        if cls._instance:
            raise Exception("Instance already configured")
        app = cls.__new__(cls)
        cls._instance = app

        setup_logging()

        #### setup app variables
        pygame.init()
        pygame.font.init() # really needed?
        app.clock = pygame.time.Clock()



        _info = pygame.display.Info()
        app.width, app.height = _info.current_w, _info.current_h

        if platform.system() == "Darwin":
            app.height -= 34 # TODO - this is a hack for the macbook air menu bar / camera cutout

            app.screen = pygame.display.set_mode((app.width // 1.8, app.height // 1.8), flags=pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SRCALPHA)
            # this 'hack' ensures that the newly created window becomes active
            time.sleep(0.1)
            pygame.display.toggle_fullscreen()
            time.sleep(0.1)
            pygame.display.toggle_fullscreen()
        else:
            app.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        pygame.display.set_allow_screensaver(False)



        return cls._instance


    def start(self):
        dotenv.load_dotenv(helpers.HERE.parent / ".env")
        helpers.assert_env()
        self.running = True

        pygame.init()
        pygame.mixer.init()

        # Set up the display
        # screen_width, screen_height = 600, 600
        # screen = pygame.display.set_mode((screen_width, screen_height))
        # pygame.display.set_caption("Fren")

        font = pygame.font.Font(None, 40)

        # ready_tone = pygame.mixer.Sound("./bling.mp3")
        ready_tone = pygame.mixer.Sound( helpers.get_resource("bling.mp3") )
        recorder = AudioRecorder()
        record_thread = None

        # global OpenAIClient
        helpers.OpenAIClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT and not recorder.is_recording:
                        ready_tone.play()
                        time.sleep(0.2) #TODO get len and sleep for that amount
                        record_thread = threading.Thread(target=recorder.start_recording)
                        record_thread.start()

                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT and recorder.is_recording:
                        recorder.is_recording = False
                        # recorder.stop_recording()
                        ready_tone.play()
                        record_thread.join()

                elif event.type == pygame.QUIT:
                    running = False

            ### END EVENT LOOP ###

            # Fill the screen with a color
            self.screen.fill((25, 55, 35))

            # Render the text
            text = font.render("Hold [SHIFT] to record your question!", True, (200, 200, 100))
            text_rect = text.get_rect(center=(300, 300))
            self.screen.blit(text, text_rect)

            # Update the display
            pygame.display.flip()

        pygame.quit()

    def stop(self):
        self.running = False
