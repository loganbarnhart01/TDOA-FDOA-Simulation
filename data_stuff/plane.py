import numpy as np

class Plane:
	def __init__(self, icao24, latitude, longitude, time_position, on_ground):
		self.icao24 = icao24
		self.latitude = latitude
		self.longitude = longitude
		self.time_position = time_position
		self.on_ground = on_ground
		self.direction = np.random.random() * 2*np.pi

	def update(self, prob= 0.1):
		if np.random.random() < prob:
			self.direction = np.random.random() * 2*np.pi
		self.latitude = max(min((self.latitude + np.sin(self.direction)), 90), -90)
		self.longitude = (self.longitude + np.cos(self.direction)) % 360 - 180
		self.time_position += 1
		self.on_ground = False

def create_planes(num_planes=10):
	planes = []
	for i in range(num_planes):
		lat = np.random.random() * 180 - 90
		lon = np.random.random() * 360 - 180
		planes.append(Plane(i, lat, lon, 1, False))

	return planes

def update_planes(planes):
	for p in planes:
		p.update()

	return planes