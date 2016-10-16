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
import threading

dict = {} #guarda ultimas posicoes dos onibus 

conf = SparkConf()

#conf.setMaster("yarn-client")

sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)

sqlContext.setConf("hive.exec.dynamic.partition.mode", "nonstrict")

num_pontos = 5 #numero de pontos para olhar para tras

grid = {} #guarda posicoes das trajetorias ja conhecidas

div = 10000 #numero pelo qual dividir lats e longs

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

def carrega_linha(linha_num):
	f = open("/home/Natalia/tcc/{linha_num}.csv".format(linha_num = linha_num))
	f.readline()
	for ponto in f:
		lat = float(ponto.split(" ")[0].split("(")[1])
		lng = float(ponto.split(" ")[1].split(")")[0])
		grid[str(lat/div)+","+str(lng/div)] = (linha_num,lat,lng)

def carrega_grid():
	carrega_linha("422")
	carrega_linha("298")
	#rot = sc.textFile("file:///home/Natalia/tcc/422.csv")
	#rflt = rot.filter(lambda x: len(x) > 11) #elimina header
	#rmp = rflt.map(lambda x: ("864",(float(x.split(" ")[1].split(")")[0]),float(x.split(" ")[0].split("(")[1])))).cache()

carrega_grid()

while(True):
	for ordem in dict:
		if len(ordem["dados"]) == num_pontos:
			linha = acha_linha(ordem["dados"])