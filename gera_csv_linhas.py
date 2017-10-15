linha = "422"

f = open("linhas/boas/"+linha+".csv")
fw = open("linhas/boas/csv_"+linha+".csv","w")

for l in f:
	try:
		lng = l.split(" ")[0].split("(")[1]
		lat = l.split(" ")[1].split(")")[0]
		fw.write(lat+";"+lng+"\n")
	except Exception,e: print str(e)

fw.close()
f.close()