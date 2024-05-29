from flask import Flask, render_template
import numpy as np
from globe_rendering_utils import render_plot  

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    return render_template('upload.html')

@app.route('/live', methods=['GET'])
def live():
    return render_template('live.html')

@app.route('/live-data', methods=['GET', 'POST'])
def live_data():
    random_data = {'lat': [np.random.random() * 180 - 90 for i in range(10)], 
                     'lon': [np.random.random() * 360 - 180 for i in range(10)], 
                     'mode' : 'markers'}
    globe_json = render_plot( random_data )
    return globe_json

if __name__ == "__main__":
    app.run(debug=True)