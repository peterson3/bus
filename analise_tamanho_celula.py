from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def distance_to_point(p1,p2):
	return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

f = open("326a.csv")

anterior_lat = -1

l = []

for ponto in f:
	try:
		lng = float(ponto.split(" ")[0].split("(")[1])
		lat = float(ponto.split(" ")[1].split(")")[0])
		if(anterior_lat != -1):
			distancia = haversine(lng,lat,anterior_lng,anterior_lat)
			#print distancia
			l.append(distancia)
		anterior_lat = lat
		anterior_lng = lng
	except:
		print "a"

print sum(l)/len(l)