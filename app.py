from flask import Flask, request, render_template
from openai_utils import handle_message
from prompt_maker import MuseumPrompt
from text_to_speech import read_text

from threading import Thread

app = Flask(__name__)

current_author = None 
current_question = None
audio_thread = None

def read_response(response):
    print("Response:", response) 
    read_text(response, "") 

@app.route('/update_author')
def update_author():
    # here we want to get the value of user (i.e. ?user=some-value)
    current_author = request.args.get('author')
    return f"Current author is: {current_author}"

@app.route('/ask_question')
def ask_question():
    current_question = request.args.get('question')
    prompt = MuseumPrompt.get_prompt(current_question)
    print("Prompt:", prompt) 
    response = handle_message(prompt, "") 
    audio_thread = Thread(target=read_response, args=(response,)) 
    audio_thread.start()
    return f"Q: {current_question} A: {response}"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    