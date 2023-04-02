from flask import Flask, request, render_template
from openai_utils import handle_message
from prompt_maker import MuseumPrompt, AuthorPrompt
from text_to_speech import read_text

from threading import Thread
import urllib.parse
import os

app = Flask(__name__)

OPENAI_KEY =os.environ["OPENAI_KEY"] 
ELEVEN_KEY = os.environ["ELEVEN_KEY"]
current_author = None 
current_question = None
audio_thread = None

def read_response(response):
    print("Response:", response) 
    read_text(response, ELEVEN_KEY) 

@app.route('/ask_question')
def ask_question():
    current_question = request.args.get('question')
    current_author = urllib.parse.unquote(request.args.get('author_name')).replace('"', '')
    print(current_author) 
    prompt = AuthorPrompt.get_prompt(current_question, author_name=current_author)
    print("Prompt:", prompt) 
    response = handle_message(prompt, OPENAI_KEY) 
    audio_thread = Thread(target=read_response, args=(response,)) 
    audio_thread.start()
    return f"Q: {current_question} A: {response}"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    