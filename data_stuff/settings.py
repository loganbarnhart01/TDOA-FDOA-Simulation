from sqlalchemy.engine import URL

def create_url():
    url = URL.create(
        drivername="postgresql",
        username="$USERNAME",
        password="$PASSWORD",
        host="/var/run/postgresql/",
        database="adsb_data"
    )

    return url