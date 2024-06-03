from sqlalchemy.engine import URL

def create_url():
    url = URL.create(
        drivername="postgresql",
        username="ehong",
        password="Elanlofr0gs!",
        host="/var/run/postgresql/",
        database="adsb_data"
    )

    return url