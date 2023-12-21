import os
import pyaudio
from pydub import AudioSegment

from helpers import *

# Audio Recording Class
class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.stream = self.audio.open(format=self.format, channels=self.channels, 
                                      rate=self.rate, input=True, frames_per_buffer=self.chunk)
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        
        self.stream.stop_stream()
        self.stream.close()
        # self.audio.terminate()

        sound = AudioSegment(data=b''.join(self.frames), sample_width=self.audio.get_sample_size(self.format),
                             frame_rate=self.rate, channels=self.channels)
        sound.export("user_recording.mp3", format="mp3")

        transcription = transcribe_audio()

        # input_dict = {"input": transcription, "user_name": "Micah"}
        input_dict = {"input": transcription}
        result = run_flow(input_dict, flow_id=os.getenv("FLOW_ID"), tweaks=TWEAKS)

        logger.info(result)

        try:
            speak(result['result']['output'])
        except KeyError:
            speak(f"Something is wrong with my code... {result['detail']}", voice=OpenAIVoices[3])
