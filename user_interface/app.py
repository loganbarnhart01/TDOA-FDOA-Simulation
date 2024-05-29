from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route('/live', methods=['GET'])
def live():
    return render_template('live_completed.html')

if __name__ == "__main__":
    app.run(debug=True)