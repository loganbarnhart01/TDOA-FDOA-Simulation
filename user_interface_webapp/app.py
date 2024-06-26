
import logging
import os
import requests
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from user_interface_webapp.globe_rendering_utils import render_live_plot, render_tdoa_plot #defined in globe rendering utils.py - called in appy.py
#take dictionary with relevant info an imports it , 
#TODO create TOGGLE to switch between plotly and non plotly globe rendering

from data_stuff.crud import read_flights
from data_stuff.database_utils import create_url

load_dotenv()

url = create_url()
engine = create_engine(url)
Session = sessionmaker(bind=engine)
db = Session()

app = Flask(__name__, static_folder='static', template_folder='templates')
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
def home():
    return render_template('index_live.html')

@app.route('/home', methods=['GET'])
def go_home():
    return render_template('index_live.html')

@app.route('/what', methods=['GET'])
def what():
    return render_template('what.html')

@app.route('/who', methods=['GET'])
def who():
    return render_template('what.html')

@app.route('/why', methods=['GET'])
def why():
    return render_template('why.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route('/live', methods=['GET'])
def live():
    return render_template('cesium_globe.html')

# @app.route('/custom-geo', methods=['GET'])
# def custom_geo():
#     return render_template('custom_geo.html')

@app.route('/live-data', methods=['GET', 'POST'])
def live_data():
    data = read_flights()
    globe_json = render_live_plot( data )
    return globe_json

@app.route('/tdoa-sim', methods=['GET'])
def tdoa_sim():
    return render_template('tdoa_sim.html')

@app.route('/tdoa-data', methods=['GET', 'POST'])
def tdoa_data():
    input_data = request.json
    globe_json = render_tdoa_plot(input_data)
    return globe_json

@app.route('/get-elevation', methods=["POST"])
def get_elevation():
    data = request.json
    lat, lon = data['latitude'], data['longitude']
    
    api_key = os.getenv( 'GOOGLE_API_KEY' )
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lon}&key={api_key}'
    
    response = requests.get(url)
    elevation = response.json()['results'][0]['elevation']

    return jsonify({'elevation' : elevation})

if __name__ == "__main__":
    app.run(debug=True)

