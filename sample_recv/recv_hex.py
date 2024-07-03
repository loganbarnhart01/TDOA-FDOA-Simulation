import socket
import pyModeS as pms
import psycopg2
from datetime import datetime
import time

def process_data(data, cursor):
    print("ICAO: " + pms.icao(data))
    ## print(data)
    update_flight(data, cursor)

    

def update_flight(data, cursor):
    dt = datetime.now()
    timestamp = int(time.mktime(dt.timetuple()))
    cursor.execute('''
        SELECT 1 FROM data WHERE icao = %s
    ''', (pms.icao(data),))
    if cursor.fetchone() is None:                               ## flight does not exist yet
        if ~(pms.decoder.adsb.oe_flag(data)):                   ## 54th bit denotes whether a bit is even or odd (0 and 1, respectively)       
            create_flight(cursor, pms.icao(data), data, None, None, None, timestamp, None)
        else:                                                   ## data must be odd
            create_flight(cursor, pms.icao(data), None, data, None, None, None, timestamp)
    else:
        if (pms.decoder.adsb.oe_flag(data)):                    ## data is even
            cursor.execute('''
                UPDATE data
                SET last_even = %s, even_timestamp = %s
                WHERE icao = %s
                ''', (data, timestamp, pms.icao(data)))

            cursor.execute('''
                SELECT last_odd, odd_timestamp FROM data WHERE icao = %s
                ''', (pms.icao(data),))
            result = cursor.fetchone()
            if result is not None:
                last_odd, odd_timestamp = result
                lati, longi = pms.decoder.adsb.position(data, last_odd, timestamp, odd_timestamp)[:2]
                print("Latitude: " + str(lati) + ", Longitude: " + str(longi))
                cursor.execute('''
                UPDATE data
                SET latitude = %s, longitude = %s
                WHERE icao = %s
                ''', (lati, longi, pms.icao(data)))
                
        else:                                                   ## data is odd
            cursor.execute('''
                UPDATE data
                SET last_odd = %s, odd_timestamp = %s
                WHERE icao = %s
                ''', (data, timestamp, pms.icao(data)))
            if cursor.execute('''
                SELECT last_even, even_timestamp FROM data WHERE icao = %s
                ''', (pms.icao(data),)):
                result = cursor.fetchone()
                if result is not None:
                    last_even, even_timestamp = result
                    lati, longi = pms.decoder.adsb.position(last_even, data, even_timestamp, timestamp)[:2]

                    cursor.execute('''
                    UPDATE data
                    SET latitude = %s, longitude = %s
                    WHERE icao = %s
                    ''', (lati, longi, pms.icao(data)))
        

def create_flight(cursor, icao, last_even, last_odd, latitude, longitude, even_timestamp, odd_timestamp):
    cursor.execute('''
        INSERT INTO data (icao, last_even, last_odd, latitude, longitude, even_timestamp, odd_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (icao, last_even, last_odd, latitude, longitude, even_timestamp, odd_timestamp))

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 30001))
    server_socket.listen(1)

    client_socket, client_address = server_socket.accept()

    conn = psycopg2.connect(database="planes", user="ehong", password="Elanlofr0gs!", host="/var/run/postgresql", port="5432")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            icao TEXT PRIMARY KEY NOT NULL,
            last_even TEXT DEFAULT NULL,
            last_odd TEXT DEFAULT NULL,
            latitude REAL DEFAULT NULL,
            longitude REAL DEFAULT NULL,
            even_timestamp INTEGER DEFAULT NULL,
            odd_timestamp INTEGER DEFAULT NULL
        )
        ''')

    try:
        while 1:
            data = client_socket.recv(1024)
            data = data.decode('utf-8')[1:]
            data = data.split('*')
            for data in data:
                if (pms.typecode(data) > 5 and pms.typecode(data) < 23 and pms.typecode(data) != 19):
                    process_data(data, cursor) 
            conn.commit()
    except KeyboardInterrupt:
        print("\nInterrupted, closing sockets.")
    finally:
        conn.close()
        client_socket.close()
        server_socket.close()

if (__name__ == "__main__"):
    main()