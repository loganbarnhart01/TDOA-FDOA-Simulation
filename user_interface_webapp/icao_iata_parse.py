import csv

def parse_airport_data(file_path):
    airports = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        for row in reader:
            country_code, region_name, iata, icao, airport, latitude, longitude = row
            airport_info = {
                "country_code": country_code,
                "region_name": region_name,
                "iata": iata,
                "icao": icao,
                "airport": airport,
                "latitude": float(latitude),
                "longitude": float(longitude)
            }
            airports.append(airport_info)
    return airports

file_path = "iata-icao-lat-lon.csv" 
airport_data = parse_airport_data(file_path)
for airport in airport_data:
    print(airport)