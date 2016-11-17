import sys
import gmplot
import urllib
import time
import os
from collections import deque
import threading

dict = {} #guarda ultimas posicoes dos onibus 
dict_linhas = {} #guarda linhas descobertas
grid = {} #guarda posicoes das trajetorias ja conhecidas

lock = threading.RLock()

num_pontos = 5 #numero de pontos para olhar para tras

n_dec = '3' #numero de casas decimais da key

def encontrar_linhas():
	with lock:
		for ordem in dict:
				if len(dict[ordem]["dados"]) == num_pontos:
					linha = acha_linha_2(dict[ordem]["dados"])
					if linha != "":
						print "ordem {ordem} pertence a linha {linha}".format(ordem = ordem, linha = linha)
						dict_linhas[ordem] = linha

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
				print linha + "Linha Inicial" #linha inicial caira aqui
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
						print "Index Error"
		time.sleep(60)

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

def acha_linha_2(pontos):
	dict_d_linhas = {}
	for ponto in pontos:
		lat = ponto[0]
		lng = ponto[1]
		key = format(lat,'.'+n_dec+'f')+","+format(lng,'.'+n_dec+'f')
		if key in grid:
			possibilidades = grid[key]
			for ponto in possibilidades:
				p_linha = ponto[0]
				p_lat = ponto[1]
				p_lng = ponto[2]
				d_lat = abs(p_lat - lat)
				d_long = abs(p_lng - lng)
				d = d_lat + d_long
				if p_linha not in dict_d_linhas:
					dict_d_linhas[p_linha] = (d,1)
				else:
						dict_d_linhas[p_linha] = (dict_d_linhas[p_linha][0] + d,dict_d_linhas[p_linha][1] + 1)
	melhor_linha = ""
	menor_media = 999999
	for linha in dict_d_linhas:
		hits = dict_d_linhas[linha][1]
		if hits >= num_pontos *0.8:
			media = dict_d_linhas[linha][0] / hits 
			if media < menor_media:
				menor_media = media
				melhor_linha = linha
	return melhor_linha

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
	carrega_linha("864a")
	carrega_linha("864b")
	carrega_linha("326a")
	carrega_linha("326b")

def t_encontrar_linhas():
	while True:
		start = time.time()
		encontrar_linhas()
		finish = time.time()
		if finish - start < 60:
			time.sleep(60 - (finish - start))
		else:
			print "encontrar linhas demorou mais que 60 segundos"


threading.Thread(target = get_dados).start()
threading.Thread(target = t_encontrar_linhas).start()

carrega_grid()



#gravar posicoes em arquivo p teste
f = open("dict.txt","w")
f.write("chave;linha;latitude;longitude")
with lock:
	for chave in dict:
		try:
			dados = dict[chave]["dados"]
			for coord in dados:
				lati = str(coord[0])
				longi = str(coord[1])
				f.write(chave+";"+dict_linhas[chave]+";"+lati + ";" + longi + "\n")
		except:
			print chave

f.close()

#gravar posicoes de uma so ordem
f = open("dict.txt","w")
dados = dict["B25515"]["dados"]
for coord in dados:
	lati = str(coord[0])
	longi = str(coord[1])
	f.write(lati + " " + longi + " ")

f.close()

#gravar linhas em csv formatado
fw = open("linhas.txt","w")
for linha in ["422","298","864a","864b","326a","326b"]:
	fw.write("chave;linha;latitude;longitude\n")
	f = open("/home/Natalia/tcc/{linha_num}.csv".format(linha_num = linha))
	f.readline()
	for ponto in f:
		lng = ponto.split(" ")[0].split("(")[1]
		lat = ponto.split(" ")[1].split(")")[0]
		fw.write(linha+";"+linha+";"+lat+";"+lng+"\n")

fw.close()