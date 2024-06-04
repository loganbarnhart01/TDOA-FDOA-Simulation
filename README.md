# Flight Tracker Simulator
Rincon 2024 Intern Project
Kelly, Elsa, Elizabeth & Logan

# installing requirements

* `pip install -e opensky-api/`
* `pip install -r requirements.txt`
* Follow postgres install instructions in `/flight_data/README.md`
* Update the user and password information in `data_stuff/settings.py` to match your postgres installation
* Generate a [Google Elevations API key](https://developers.google.com/maps/documentation/elevation/start) and store it in a file called `.env` in the root directory of the project. The file should contain the following text: `GOOGLE_API_KEY=\<your_api_key_here\>`

# How to run the application:
* To collect live data, run `python -m data_stuff.data_collector &` in the background, note the PID if you'd like to kill it later
* To run the web application, run `python -m user_interface_webapp.app``
