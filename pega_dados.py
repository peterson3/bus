import urllib
import time
import os

dict = {}

while (True):
	urllib.urlretrieve ("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm", "/home/SVA/teste/bus.txt")
	fr = open("/home/SVA/teste/bus.txt")
	fw = open("/home/SVA/teste/bus2.txt","w")
	for linha in fr:
		campos = linha.split(",")
		ordem = campos[1]
		data = campos[0]
		try:
			if data != dict[ordem]:
				dict[ordem] = data
				fw.write(linha)
		except:
			dict[ordem] = data
			fw.write(linha)
	filename = "bus"+str(time.time())+".txt"
	os.system('hdfs dfs -put /home/SVA/teste/bus2.txt /teste/'+filename)
	time.sleep(60)

