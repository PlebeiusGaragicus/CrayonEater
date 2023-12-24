import os
import threading
import queue
import time

import json
import pyaudio
from pydub import AudioSegment

import logging
logger = logging.getLogger()

from fren import helpers
from fren.workflow import run_flow, transcribe_audio, speak
from fren.audio import audio

# Audio Recording Class
class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        self._is_recording = False
        self._lock = threading.Lock()
        self.queue = queue.Queue()
        self.queue.put('ready')

        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None

    @property
    def is_recording(self):
        with self._lock:
            return self._is_recording
    
    @is_recording.setter
    def is_recording(self, value):
        with self._lock:
            self._is_recording = value


    def start_recording(self):

        # audio().dink_effect.play()
        audio().dink()
        time.sleep(0.2)


        ###########################
        self.queue.put('recording')
        self.is_recording = True

        self.frames = []
        self.stream = self.audio.open(format=self.format, channels=self.channels, 
                                      rate=self.rate, input=True, frames_per_buffer=self.chunk)


        while self.is_recording:
            data = self.stream.read(self.chunk)
            if not self.is_recording:
                break
            self.frames.append(data)


        ##############################
        self.queue.put('transcribing')
        self.stream.stop_stream()
        self.stream.close()
        # self.audio.terminate()

        runlog_dir = helpers.get_path("runlog", helpers.get_timestamp())
        #make directory
        os.makedirs(runlog_dir, exist_ok=True)

        user_recording_filename = helpers.get_path(runlog_dir, f"user_recording.mp3")
        sound = AudioSegment(data=b''.join(self.frames), sample_width=self.audio.get_sample_size(self.format), frame_rate=self.rate, channels=self.channels)
        sound.export(user_recording_filename, format="mp3")


        transcription = transcribe_audio(user_recording_filename)
        logger.info(transcription)
        with open(runlog_dir + "/user_transcription.txt", "w") as f:
            f.write(transcription)



        ##############################
        self.queue.put('thinking')

        input_dict = {"input": transcription}
        # result = run_flow(input_dict, flow_id=os.getenv("FLOW_DEMO"), tweaks=TWEAKS)
        result = run_flow(input_dict, flow_id=os.getenv("FLOW_DEMO"))

        logger.info(result)
        with open(runlog_dir + "/result.json", "w") as f:
            json.dump(result, f, indent=4)


        ##########################
        self.queue.put('speaking')
        try:
            speak(result['result']['output'], runlog_dir)
        except KeyError:
            speak(f"Something is wrong with my code... {result['detail']}", voice=helpers.OpenAIVoices[3])

        #######################
        self.queue.put('ready')
