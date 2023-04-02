import time
import threading
import simpleaudio as sa
from pydub import AudioSegment

class AudioPlaybackThread(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename
        self.stop_event = threading.Event()

    def run(self):
        # # load the mp3 file and convert it to WAV format
        mp3 = AudioSegment.from_mp3(self.filename)
        mp3 = mp3 - 23 
        wave_data = mp3.export(format="wav").read()
        # create a Simpleaudio buffer from the wave data
        play_obj = sa.play_buffer(wave_data, num_channels=2, bytes_per_sample=2, sample_rate=44100)
        # wait for the playback to finish or stop_event to be set
        while not self.stop_event.is_set():
            if not play_obj.is_playing():
                play_obj = sa.play_buffer(wave_data, num_channels=2, bytes_per_sample=2, sample_rate=44100)
            time.sleep(0.1)
        play_obj.stop()
        
    def stop(self):
        self.stop_event.set()
