import gmplot
import googlemaps
from datetime import datetime

f = open("/home/Natalia/tcc/dict.txt")

lat = []
lng = []

for linha in f:
	spl = linha.split()
	o = float(spl[1])
	lng.append(o)
	a = float(spl[0])
	lat.append(a)

#grava o html

gmap = gmplot.GoogleMapPlotter(-22.875641699999999,-43.4688534, 16)

gmap.scatter(lat, lng, '#3B0B39', size=50, marker=False)

gmap.draw("/home/Natalia/tcc/mymap.html")