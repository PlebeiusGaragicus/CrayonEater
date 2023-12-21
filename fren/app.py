import os
import threading
import time
import json
import base64
import asyncio
import requests
from typing import Optional

import pyaudio
import dotenv
import pygame
import assemblyai as aai
from openai import OpenAI

from helpers import *



def main():
    dotenv.load_dotenv(HERE.parent / ".env")
    assert_env()

    pygame.init()
    pygame.mixer.init()

    # Set up the display
    screen_width, screen_height = 600, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fren")

    font = pygame.font.Font(None, 40)

    ready_tone = pygame.mixer.Sound("./bling.mp3")
    recorder = AudioRecorder()
    record_thread = None

    global OpenAIClient
    OpenAIClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

                    # transcription = transcribe_audio()

                    # input_dict = {"input": transcription}
                    # result = run_flow(input_dict, flow_id=os.getenv("FLOW_ID"), tweaks=TWEAKS)

                    # speak(result['result']['output'])

            elif event.type == pygame.QUIT:
                running = False

        ### END EVENT LOOP ###

        # Fill the screen with a color
        screen.fill((25, 55, 35))

        # Render the text
        text = font.render("Hold [SHIFT] to record your question!", True, (200, 200, 100))
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

    pygame.quit()


