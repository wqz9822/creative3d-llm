from elevenlabslib import *
import re

def split_paragraph_into_sentences(paragraph):
    sentence_enders = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
          (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        \s+               # Split on whitespace between sentences.
        """, 
        re.IGNORECASE | re.VERBOSE)
    sentences = sentence_enders.split(paragraph)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def group_sentences(lst, chunk_size):
    chunks = []
    for i in range(0, len(lst), chunk_size):
        chunks.append(lst[i:i + chunk_size])
    return chunks

def read_text(text, api_key, streaming=False):
    user = ElevenLabsUser(api_key)
    voice = user.get_voices_by_name("Rachel")[0]  # This is a list because multiple voices can have the same name
    if streaming:
        voice.generate_and_stream_audio(text, stability=0.5, streamInBackground=False)
    else:
        voice.generate_and_play_audio(text, stability=0.5, playInBackground=False)
