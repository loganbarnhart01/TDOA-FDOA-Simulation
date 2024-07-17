from opensky_api import OpenSkyApi
import pandas as pd

api = OpenSkyApi()
states = api.get_states().states

state_dicts = [s.__dict__ for s in states]

df = pd.DataFrame(state_dicts)
df.to_csv('adsb_data.csv')