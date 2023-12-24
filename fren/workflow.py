import os
import datetime
from typing import Optional
import requests
import pygame
import assemblyai as aai

from fren import helpers

import logging
logger = logging.getLogger()




def transcribe_audio(filename):
    logger.info("Transcribing audio...")
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speaker_labels=False)
    # transcript = transcriber.transcribe(helpers.HERE / "runlog" / "user_recording.mp3", config) #TODO
    # transcript = transcriber.transcribe("./user_recording.mp3", config)
    transcript = transcriber.transcribe(filename, config)

    logger.debug(transcript.text)

    return transcript.text



def speak(input: str, runlog_dir, voice = helpers.OpenAIVoices[4]):
    # global OpenAIClient

    response = helpers.OpenAIClient.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=f"{input}"
    )

    speech_file_path = helpers.get_path(runlog_dir, f"tts.mp3")
    response.stream_to_file(speech_file_path)

    # play the file with pygame
    tts = pygame.mixer.Sound(speech_file_path)
    tts.play()






# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "OpenAIConversationalAgent-0HJdd": {},
  "PythonFunctionTool-uJfF3": {}
}

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param flow_id: The ID of the flow to run
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{os.getenv('BASE_API_URL')}/{flow_id}"

    payload = {"inputs": inputs}
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload, headers=headers)

    # response = requests.post(api_url, json=payload, headers=headers, stream=True)
    # get each streamed event
    # for line in response.iter_lines():
    #     if line:
    #         decoded_line = line.decode('utf-8')
    #         event = json.loads(decoded_line)
    #         logger.info(event)

    logger.info(response.json())

    return response.json()
