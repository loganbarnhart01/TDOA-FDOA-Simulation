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
    #generate random path
    path_len=10
    start_lats = [np.random.random() * 180 - 90 for i in range(5)]
    start_lons = [np.random.random() * 360 - 180 for i in range(5)]

    random_data = {'lat': [[start_lats[j] + np.random.random() * 10 - 5 for i in range(path_len)] for j in range(5)], 
                     'lon': [[start_lons[j] + np.random.random() * 10 - 5 for i in range(path_len)] for j in range(5)], 
                     'mode' : 'lines+markers'}
    globe_json = render_plot( random_data )
    return globe_json

if __name__ == "__main__":
    app.run(debug=True)