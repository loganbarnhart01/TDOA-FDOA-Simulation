# make table in sql
from opensky_api import OpenSkyApi
import time
import pandas as pd
import crud


def data_collector():
	crud.create_table()
	while True:
		api = OpenSkyApi()
		states = api.get_states().states

		for s in states:
			crud.create_flight(s.icao24, str(s.latitude), str(s.longitude), s.time_position, s.on_ground)

		time.sleep(10)

	
data_collector()
