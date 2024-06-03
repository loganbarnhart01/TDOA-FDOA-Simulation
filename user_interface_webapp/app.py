import logging

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from user_interface_webapp.globe_rendering_utils import render_live_plot, render_tdoa_plot
from data_stuff.crud import Flight

url = URL.create(
    drivername="postgresql",
    username="ehong",
    password="Elanlofr0gs!",
    host="/var/run/postgresql/",
    database="adsb_data"
)

engine = create_engine(url)

Session = sessionmaker(bind=engine)

db = Session()

def read_flights():
	lats = db.query(Flight.latitude).all()
	longs = db.query(Flight.longitude).all()
	data = {'lat': [list(map(float, lat[0].split(','))) for lat in lats], 'lon': [list(map(float, lon[0].split(','))) for lon in longs]}

	return data

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

if __name__ == "__main__":
    app.run(debug=True)

