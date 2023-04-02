from flask import Flask, request, render_template

app = Flask(__name__)

current_location = None 

@app.route('/update_location')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    current_location = request.args.get('location')
    return f"Current location is: {current_location}"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()