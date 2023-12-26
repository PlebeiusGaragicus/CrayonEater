import os
import threading
import queue
import time
import websockets
import asyncio
import base64

import json
import pyaudio
from pydub import AudioSegment


import logging
logger = logging.getLogger()

from fren import helpers
from fren.workflow import run_flow, transcribe_audio, speak
from fren.audio import audio





import asyncio
import websockets
import pyaudio
import base64
import json
import os

class TranscriptionService:
    def __init__(self, ar):
        self.is_recording = True  # You need a mechanism to stop recording
        self.AudioRecorder = ar
        # self.queue = asyncio.Queue()  # Queue for handling transcripts

    async def send_audio_data(self, stream, ws):
        FRAMES_PER_BUFFER = 3200
        while self.AudioRecorder.is_recording:
            try:
                data = stream.read(FRAMES_PER_BUFFER)
                data = base64.b64encode(data).decode("utf-8")
                json_data = json.dumps({"audio_data": str(data)})
                await ws.send(json_data)
            except Exception as e:
                print(f"Error sending audio data: {e}")
                break
            await asyncio.sleep(0.01)

    async def receive_transcription(self, ws):
        final_transcript = ""
        # while self.AudioRecorder.is_recording:
        is_recording = True
        while is_recording:
            try:
                result_str = await ws.recv()
                result = json.loads(result_str)
                if result['message_type'] == 'FinalTranscript':
                    final_transcript = result['text']
                    # self.is_recording = False  # Stop recording on final transcript
                    is_recording = False  # Stop recording on final transcript
                    self.AudioRecorder.queue.put_nowait({"text": result['text']})

                elif result['message_type'] == 'PartialTranscript':
                    self.AudioRecorder.queue.put_nowait({"text": result['text']})
                    # self.queue.put({"text": result['text']})
            except Exception as e:
                print(f"Error receiving transcription: {e}")
                break
        logger.info(final_transcript)
        return final_transcript



    async def send_receive(self, stream):
        RATE = 16000
        URL = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={RATE}"

        print(f'Connecting websocket to url {URL}')
        async with websockets.connect(
            URL,
            extra_headers=(("Authorization", os.getenv("ASSEMBLYAI_API_KEY")),),
            ping_interval=5,
            ping_timeout=20
        ) as ws:
            send_task = asyncio.create_task(self.send_audio_data(stream, ws))
            receive_task = asyncio.create_task(self.receive_transcription(ws))

            final_transcript = await receive_task
            send_task.cancel()  # Cancel the sending task as we have the final transcript
            return final_transcript

    def realtime_transcription(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=3200
        )

        try:
            final_transcript = ''
            while self.AudioRecorder.is_recording:
                final_transcript += asyncio.run(self.send_receive(stream)) + ' '

            return final_transcript
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            # TODO - catch a null return














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



    ########################################
    def record_transcribe(self, runlog_dir):
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

        user_recording_filename = helpers.get_path(runlog_dir, f"user_recording.mp3")
        sound = AudioSegment(data=b''.join(self.frames), sample_width=self.audio.get_sample_size(self.format), frame_rate=self.rate, channels=self.channels)
        sound.export(user_recording_filename, format="mp3")


        transcription = transcribe_audio(user_recording_filename)
        logger.info(transcription)
        self.queue.put({"text": transcription})



    #################################
    # def realtime_transcription(self):
    #     FRAMES_PER_BUFFER = 3200
    #     FORMAT = pyaudio.paInt16
    #     CHANNELS = 1
    #     RATE = 16000
    #     p = pyaudio.PyAudio()

    #     # Open an audio stream with above parameter settings
    #     stream = p.open(
    #         format=FORMAT,
    #         channels=CHANNELS,
    #         rate=RATE,
    #         input=True,
    #         frames_per_buffer=FRAMES_PER_BUFFER
    #     )


    #     # Send audio (Input) / Receive transcription (Output)
    #     async def send_receive():
    #         URL = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={RATE}"

    #         print(f'Connecting websocket to url ${URL}')

    #         async with websockets.connect(
    #             URL,
    #             extra_headers=(("Authorization", os.getenv("ASSEMBLYAI_API_KEY")),),
    #             ping_interval=5,
    #             ping_timeout=20
    #         ) as _ws:

    #             r = await asyncio.sleep(0.1)
    #             print("Receiving messages ...")

    #             session_begins = await _ws.recv()
    #             # print(session_begins)
    #             # print("Sending messages ...")


    #             async def send():
    #                 while self.is_recording:
    #                     try:
    #                         data = stream.read(FRAMES_PER_BUFFER)
    #                         data = base64.b64encode(data).decode("utf-8")
    #                         json_data = json.dumps({"audio_data":str(data)})
    #                         r = await _ws.send(json_data)

    #                     except websockets.exceptions.ConnectionClosedError as e:
    #                         print(e)
    #                         assert e.code == 4008
    #                         break

    #                     except Exception as e:
    #                         print(e)
    #                         assert False, "Not a websocket 4008 error"

    #                     r = await asyncio.sleep(0.01)


    #             async def receive():
    #                 while self.is_recording:
    #                     try:
    #                         result_str = await _ws.recv()
    #                         result = json.loads(result_str)['text']

    #                         if json.loads(result_str)['message_type']=='FinalTranscript':
    #                             # self.queue.put({"text": result})
    #                             return result
    #                             # print(result)
    #                         if json.loads(result_str)['message_type']=='PartialTranscript':
    #                             self.queue.put({"text": result})

    #                     except websockets.exceptions.ConnectionClosedError as e:
    #                         print(e)
    #                         assert e.code == 4008
    #                         break

    #                     except Exception as e:
    #                         print(e)
    #                         assert False, "Not a websocket 4008 error"
                    
    #         send_result, receive_result = await asyncio.gather(send(), receive())
    #         return receive_result

    #     res = asyncio.run(send_receive())

    #     return res




    def start_recording(self):
        audio().dink()
        time.sleep(0.2)

        ###########################
        self.queue.put('recording')
        self.is_recording = True

        runlog_dir = helpers.get_path("runlog", helpers.get_timestamp())

        #make directory
        os.makedirs(runlog_dir, exist_ok=True)

        # transcription = self.record_transcribe(runlog_dir)
        # transcription = self.realtime_transcription()

        transcription_service = TranscriptionService(self)
        transcription = transcription_service.realtime_transcription()

        logger.info(transcription)
        with open(runlog_dir + "/user_transcription.txt", "w") as f:
            f.write(transcription)

        ##############################
        self.queue.put('thinking')

        input_dict = {"input": transcription}
        # result = run_flow(input_dict, flow_id=os.getenv("FLOW_DEMO"), tweaks=TWEAKS)
        result = run_flow(input_dict, flow_id=os.getenv("FLOW_DEMO"))

        logger.info(result)

        try:
            self.queue.put({"text": result['result']['output']})
        except KeyError:
            self.queue.put({"text": result['detail']})

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
