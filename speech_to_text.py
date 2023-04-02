import openai
import pyaudio
import wave
import tempfile
import argparse

# Record audio from the microphone
def record_audio(filename, duration=5, rate=16000):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RECORD_SECONDS = duration

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=rate, input=True, frames_per_buffer=1024)

    print("Recording...")
    frames = []

    for _ in range(0, int(rate / 1024 * RECORD_SECONDS)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

# Transcribe audio using OpenAI Whisper API
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript

if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API key")
    args = parser.parse_args()
    
    # Set up OpenAI API key
    openai.api_key = args.api_key
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        record_audio(temp_audio_file.name)
        transcript = transcribe_audio(temp_audio_file.name)
        print("Transcript:", transcript)
