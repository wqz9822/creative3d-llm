import openai
import time
import argparse
import tempfile
import threading
import simpleaudio as sa
from pydub import AudioSegment
from openai_utils import handle_message
from speech_to_text import record_audio, transcribe_audio
from text_to_speech import read_text, split_paragraph_into_sentences, group_sentences

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

def transcribe_and_receive_response():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        record_audio(temp_audio_file.name)
        transcript = transcribe_audio(temp_audio_file.name)
        print("Transcript:", transcript)
        return handle_message(transcript["text"], args.openai_api_key) 

def read_response(response, elevenlabs_api_key): 
    if not args.elevenlabs_api_key:
        print("Skipping ElevenLabs API call as no API key was provided.") 
        return
    # groups = group_sentences(split_paragraph_into_sentences(response), 5) 
    # for group in groups: 
    #     if group: 
    #         text=" ".join(group)
    #         read_text(text, args.elevenlabs_api_key, streaming=True)
    read_text(response, args.elevenlabs_api_key, streaming=True)

# Define main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with GPT using OpenAI')
    parser.add_argument('--openai_api_key', type=str, required=True, help='the OpenAI API key to use')
    parser.add_argument('--elevenlabs_api_key',type=str, required=False, help='the ElevenLabs API key to use')
    parser.add_argument('--mute_music', action='store_true', required=False, help='mute the background music')
    args = parser.parse_args()
    # Set up OpenAI API key
    openai.api_key = args.openai_api_key

    if not args.mute_music:
        playback_thread = AudioPlaybackThread("background.mp3")
        playback_thread.start()

    while True:
        user_input = input("Press 'm' to send a message, 'r' to record audio, or 'e' to exit: ")
        # TODO: Prefix the prompt
        if user_input == 'm':
            prompt = input("Enter your message: ")
            response = handle_message(prompt, args.openai_api_key) 
            print("Response:", response) 
            read_response(response, args.elevenlabs_api_key) 
        elif user_input == 'r':
            response = transcribe_and_receive_response()
            print("Response:", response) 
            read_response(response, args.elevenlabs_api_key) 
        elif user_input == 'e':
            break
        else:
            print("Invalid input, please try again.")

    if playback_thread.is_alive():
        playback_thread.stop()
        playback_thread.join() 
