import gmplot
import googlemaps
from datetime import datetime

f = open("linhas/422.csv")

lat = []
lng = []

for linha in f:
	#print linha
	if linha != '"st_astext"\n':
		spl = linha.split()
		o = float(spl[0].split("(")[1])
		lng.append(o)
		a = float(spl[1].split(")")[0])
		lat.append(a)

#grava o html

gmap = gmplot.GoogleMapPlotter(-22.875641699999999,-43.4688534, 16)

gmap.scatter(lat, lng, '#3B0B39', size=100, marker=False)

gmap.draw("mymap.html")

#########

gmaps = googlemaps.Client(key='AIzaSyA1Ta280qT3yWu9ZnkNrDtJjUWlOSb3FYs')

now = datetime.now()
directions_result = gmaps.directions("Plaza Shopping Niteroi",
                                     "Avenida ary parreiras niteroi",
                                     mode="transit",
                                     transit_mode = "bus")
    
directions_result[0]["legs"][0]['steps'][1]['transit_details']['line']['short_name']
# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

#####agua

#https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyA1Ta280qT3yWu9ZnkNrDtJjUWlOSb3FYs
	
reverse_geocode_result = gmaps.reverse_geocode((-22.947157, -43.171191))

for item in reverse_geocode_result:
	if any(x in item for x in ['Water','Sea', 'Lake', 'Ocean']):
		print "yeah"