import openai
import argparse
import tempfile
from openai_utils import handle_message
from speech_to_text import record_audio, transcribe_audio
from text_to_speech import read_text

# Define main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with GPT using OpenAI')
    parser.add_argument('--openai_api_key', type=str, required=True, help='the OpenAI API key to use')
    parser.add_argument('--elevenlabs_api_key',type=str, required=False, help='the ElevenLabs API key to use')
    args = parser.parse_args()

    # Set up OpenAI API key
    openai.api_key = args.openai_api_key

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        record_audio(temp_audio_file.name)
        transcript = transcribe_audio(temp_audio_file.name)
        print("Transcript:", transcript)
        response = handle_message(transcript["text"], args.openai_api_key) 
        print("Response:", response) 
        if args.elevenlabs_api_key:
            read_text(response, args.elevenlabs_api_key)
        else:
            print("Skipping ElevenLabs API call as no API key was provided.") 

    
