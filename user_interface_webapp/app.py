import logging
import os
import requests
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from user_interface_webapp.globe_rendering_utils import render_live_plot, render_tdoa_plot

from data_stuff.crud import read_flights
from data_stuff.database_utils import create_url

load_dotenv()

url = create_url()
engine = create_engine(url)
Session = sessionmaker(bind=engine)
db = Session()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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
    data = read_flights()
    app.logger.debug(f"Latitude: {data['lat'][0]}, \nLongitude: {data['lon'][0]}")
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
    app.logger.debug("ELEVATION REQUEST RECEIVED \n")
    data = request.json
    lat, lon = data['latitude'], data['longitude']
    
    api_key = os.getenv( 'GOOGLE_API_KEY' )
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lon}&key={api_key}'
    
    response = requests.get(url)
    elevation = response.json()['results'][0]['elevation']

    app.logger.debug(f"Elevation: {elevation:.0f}\n")

    return jsonify({'elevation' : elevation})

if __name__ == "__main__":
    app.run(debug=True)

