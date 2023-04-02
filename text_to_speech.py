from elevenlabslib import *

def read_text(text, api_key):
    user = ElevenLabsUser(api_key)
    voice = user.get_voices_by_name("Rachel")[0]  # This is a list because multiple voices can have the same name
    voice.generate_and_play_audio(text, playInBackground=False)
