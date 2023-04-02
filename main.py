
import argparse
import tempfile
from openai_utils import handle_message
from speech_to_text import record_audio, transcribe_audio

# Define main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with GPT using OpenAI')
    parser.add_argument('--api_key', metavar='API_KEY', type=str, required=True,
                        help='the OpenAI API key to use')
    args = parser.parse_args()

    api_key = args.api_key

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        record_audio(temp_audio_file.name)
        transcript = transcribe_audio(temp_audio_file.name)
        print("Transcript:", transcript)
        response = handle_message(transcript["text"], api_key) 
        print("Response:", response) 
    
