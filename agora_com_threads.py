#from pyspark import SparkContext, SparkConf
#from pyspark.sql import SQLContext, HiveContext, Row
#from pyspark.sql.types import *  
import sys
import gmplot
#from pyspark.sql.window import Window
#import pyspark.sql.functions as func
import urllib
import time
import os
from collections import deque
import threading

dict = {} #guarda ultimas posicoes dos onibus 

lock = threading.RLock()

num_pontos = 5 #numero de pontos para olhar para tras

grid = {} #guarda posicoes das trajetorias ja conhecidas

n_dec = '3' #numero de casas decimais da key

#conf = SparkConf()

#conf.setMaster("yarn-client")

#sc = SparkContext(conf = conf)
#sqlContext = HiveContext(sc)

#sqlContext.setConf("hive.exec.dynamic.partition.mode", "nonstrict")

def get_dados():
	while(True):
		urllib.urlretrieve ("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm", "/home/SVA/teste/bus.txt")
		fr = open("/home/SVA/teste/bus.txt")
		for linha in fr:
			campos = linha.split(",")
			ordem = campos[1]
			data = campos[0]
			linha_num = campos[2]
			try:
				lat = float(campos[3].replace('"',''))
				lng = float(campos[4].replace('"',''))
			except:
				print linha #linha inicial caira aqui
			if linha_num == "":
				with lock:
					try:
						if data != dict[ordem]["ultima_data"]:
							inserir = True
							for ponto in dict[ordem]["dados"]:
								if lat == ponto[0] and lng == ponto[1]:
									inserir = False
							if inserir:
								dict[ordem]["dados"].append([lat,lng])
								if len(dict[ordem]["dados"]) > num_pontos:
									dict[ordem]["dados"].popleft()
					except KeyError:
						dict[ordem] = {}
						dict[ordem]["ultima_data"] = data
						dict[ordem]["dados"] = deque([[lat,lng]])
					except IndexError,e:
						print dict[ordem]
						print e
		time.sleep(60)

threading.Thread(target = get_dados).start()

def acha_linha(pontos):
	melhores_linhas = {}
	for ponto in pontos:
		lat = ponto[0]
		lng = ponto[1]
		key = format(lat,'.'+n_dec+'f')+","+format(lng,'.'+n_dec+'f')
		try:
			possibilidades = grid[key]
			menor_d = 99999
			melhor_linha = ""
			for ponto in possibilidades:
				p_linha = ponto[0]
				p_lat = ponto[1]
				p_lng = ponto[2]
				d_lat = abs(p_lat - lat)
				d_long = abs(p_lng - lng)
				d = d_lat + d_long
				if d < menor_d:
					menor_d = d
					melhor_linha = p_linha
			if melhor_linha in melhores_linhas:
				melhores_linhas[melhor_linha] += 1
			else:
				melhores_linhas[melhor_linha] = 1
			print possibilidades
		except KeyError:
			pass
	retorno = ""
	maior_pontuacao = 0
	for linha in melhores_linhas:
		if melhores_linhas[linha] > maior_pontuacao:
			retorno = linha
	return retorno

def carrega_linha(linha_num):
	f = open("/home/Natalia/tcc/{linha_num}.csv".format(linha_num = linha_num))
	f.readline()
	for ponto in f:
		lng = float(ponto.split(" ")[0].split("(")[1])
		lat = float(ponto.split(" ")[1].split(")")[0])
		key = format(lat,'.'+n_dec+'f')+","+format(lng,'.'+n_dec+'f')
		if key in grid:
			grid[key].append((linha_num,lat,lng))
		else:
			grid[key] = []

def carrega_grid():
	carrega_linha("422")
	carrega_linha("298")
	#rot = sc.textFile("file:///home/Natalia/tcc/422.csv")
	#rflt = rot.filter(lambda x: len(x) > 11) #elimina header
	#rmp = rflt.map(lambda x: ("864",(float(x.split(" ")[1].split(")")[0]),float(x.split(" ")[0].split("(")[1])))).cache()

carrega_grid()

dict_linhas = {}

while(True):
	with lock:
		for ordem in dict:
				if len(dict[ordem]["dados"]) == num_pontos:
					#print "ordem: "+str(ordem)+"\n"
					linha = acha_linha(dict[ordem]["dados"])
					print "ACHAMOS LINHA UHUL"
					dict_linhas[ordem] = linha
