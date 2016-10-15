import urllib
import time
import os

while (True):
	urllib.urlretrieve ("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm", "/home/SVA/teste/bus.txt")
	filename = "bus"+str(time.time())+".txt"
	os.system('hdfs dfs -put /home/SVA/teste/bus.txt /teste/'+filename)
	time.sleep(60)

