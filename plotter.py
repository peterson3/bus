gmap = gmplot.GoogleMapPlotter(-43.4688534, -22.875641699999999, 16)

#grava o html
#########

lat = flt.map(lambda x: float(x.lat)).collect()

lng = flt.map(lambda x: float(x.lon)).collect()

#grp = flt.rdd.groupBy(lambda x: x.ordem).map(lambda x : (x[0], list(x[1]).coalesce(1)

gmap = gmplot.GoogleMapPlotter(-22.875641699999999,-43.4688534, 16)

gmap.scatter(lat, lng, '#3B0B39', size=40, marker=False)

gmap.draw("mymap.html")

#########

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyA1Ta280qT3yWu9ZnkNrDtJjUWlOSb3FYs')

now = datetime.now()
directions_result = gmaps.directions("Plaza Shopping Niteroi",
                                     "Avenida ary parreiras niteroi",
                                     mode="transit",
                                     transit_mode = "bus")
    
directions_result[0]["legs"][0]['steps'][1]['transit_details']['line']['short_name']
# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')