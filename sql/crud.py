from sqlalchemy.orm import Session

db_url = "sqlite:///./planes.db" # or whatever the url is
# create engine stuff here

db = Session()

def create_plane(db : Session, plane_data: String):
    plane_data = plane_data.split()
    icao24 = plane_data[0]
    
    if db.query(plane_table).filter_by(icao24=icao24).first(): # if the plane already exists
        return
    else:
        lat = plane_data[1]
        lon = plane_data[2]
        time = plane_data[3]
        db.add(...)

def update_plane(db : Session, plane_data: String):
    plane_data = plane_data.split()
    icao24 = plane_data[0]
    plane_to_update = db.query(plane_table).filter_by(icao24=icao24).first()

    if plane_to_update is None: # if the plane does not exist
        return
    else:
        lat = plane_data[1]
        lon = plane_data[2]
        time = plane_data[3]
        new_lat = plane_to_update.lat + lat
        ....
        db.update(...)