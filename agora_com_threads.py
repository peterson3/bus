from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, HiveContext, Row
from pyspark.sql.types import *  
import sys
import gmplot
from pyspark.sql.window import Window
import pyspark.sql.functions as func
import urllib
import time
import os
from collections import deque

dict = {}

conf = SparkConf()

#conf.setMaster("yarn-client")

sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)

sqlContext.setConf("hive.exec.dynamic.partition.mode", "nonstrict")

num_pontos = 5

def get_dados():
	while(True):
		urllib.urlretrieve ("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm", "/home/SVA/teste/bus.txt")
		fr = open("/home/SVA/teste/bus.txt")
		for linha in fr:
			campos = linha.split(",")
			ordem = campos[1]
			data = campos[0]
			linha = campos[2]
			lat = campos[3]
			lng = campos[3]
			if linha == "":
				try:
					if data != dict[ordem]["ultima_data"]:
						dict[ordem]["dados"].append([lat,lng])
						if len(dict[ordem]["dados"]) > num_pontos:
							dict[ordem]["dados"].popleft()
				except KeyError:
					dict[ordem]["ultima_data"] = data
					dict[ordem]["dados"] = deque([[lat,lng]])
		time.sleep(60)

threading.Thread(target = get_dados).start()

def acha_linha(pontos):
	for ponto in pontos:
		

while(True):
	for ordem in dict:
		if len(ordem["dados"]) == num_pontos:
			linha = acha_linha(ordem["dados"])