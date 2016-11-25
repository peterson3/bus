import sys
import gmplot
import urllib
import time
import os
from collections import deque
import threading
import web

urls = ('/linhas', 'list_linhas','/linhas/(.*)', 'get_linha')

dict_ordem = {} #guarda info de ordens ----> dict_ordem[ordem]["pontos"/"ultima_data"/"linha"]
dict_linha = {} #guarda ordens relativas e uma linha ----> dict_linha[linha] = [ordens]
grid = {} #guarda posicoes das trajetorias ja conhecidas ----> grid[key].append((linha_num,lat,lng))

lock = threading.RLock()

num_pontos = 5 #numero de pontos para olhar para tras

n_dec = '3' #numero de casas decimais da key

def remove_ordem(ordem): #remove ordem do dict_linha
	counter = 0
	for linha in dict_linha:
		if ordem in dict_linha[linha]:
			dict_linha[linha].remove(ordem)
			counter += 1
	if counter > 1:
		print "removidas {n} ocorrencias da ordem {ordem}. Isso nao devia ter acontecido".format(n = counter, ordem = ordem)

def encontrar_linhas():
	with lock:
		for ordem in (ordem for ordem in dict_ordem if dict_ordem[ordem]["linha"]["confiavel"] == False):
				if len(dict_ordem[ordem]["pontos"]) == num_pontos:
					linha = acha_linha_2(dict_ordem[ordem]["pontos"])
					if linha != "":
						print "ordem {ordem} pertence a linha {linha}".format(ordem = ordem, linha = linha)
						#verifica se linha mudou p/ atualizar dicionarios
						if ordem in dict_ordem:
							linha_antiga = dict_ordem[ordem]["linha"]["num"]
							print linha_antiga + " linha antiga, linha nova: " + linha
							if linha_antiga != linha:	
								dict_ordem[ordem]["linha"]["num"] = linha
								dict_ordem[ordem]["linha"]["confiavel"] = False
								if linha_antiga != '':
									dict_linha[linha_antiga].remove(ordem)
						else:
							print "ordem {ordem} nao estava no dicionario".format(ordem = ordem)
						if linha in dict_linha:
							if ordem not in dict_linha[linha]:
								dict_linha[linha].append(ordem)
						else:
							dict_linha[linha] = [ordem]

def get_dados():
	while(True):
		start = time.time()
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
				continue
			if linha_num == "": #linha nao informada
				with lock:
					if ordem in dict_ordem:
						if data != dict_ordem[ordem]["ultima_data"]: #posicao eh nova
							#verifica se onibus se moveu. no futuro adicionar distancia minima de movimento
							inserir = True
							for ponto in dict_ordem[ordem]["pontos"]:
								if lat == ponto[0] and lng == ponto[1]:
									inserir = False
							if inserir:
								#dict_ordem[ordem]["linha"]["num"] = ""
								dict_ordem[ordem]["linha"]["confiavel"] = False 
								dict_ordem[ordem]["pontos"].append([lat,lng])
								dict_ordem[ordem]["ultima_data"] = data
								dict_ordem[ordem]["info"] = campos
								if len(dict_ordem[ordem]["pontos"]) > num_pontos: #lista de pontos atingiu o limite de pontos analisados
									dict_ordem[ordem]["pontos"].popleft()
					else:
						dict_ordem[ordem] = {}
						dict_ordem[ordem]["ultima_data"] = data
						dict_ordem[ordem]["pontos"] = deque([[lat,lng]])
						dict_ordem[ordem]["linha"] = {}
						dict_ordem[ordem]["linha"]["num"] = ""
						dict_ordem[ordem]["linha"]["confiavel"] = False
						dict_ordem[ordem]["info"] = campos
			else: #if linha_num != '' se linha foi informada
				#tira ordem da linha anterior
				remove_ordem(ordem)
				#inclui ordem na nova linha
				if linha_num not in dict_linha: #linha nao esta no dicionario
					dict_linha[linha_num] = [ordem]
				else:
					dict_linha[linha_num].append(ordem)
				#inclui/atualiza ordem no dict_ordem
				if ordem not in dict_ordem: #ordem nao esta no dicionario
					dict_ordem[ordem] = {}
					dict_ordem[ordem]["ultima_data"] = data
					dict_ordem[ordem]["pontos"] = deque([[lat,lng]])
					dict_ordem[ordem]["linha"] = {}
					dict_ordem[ordem]["linha"]["num"] = linha_num
					dict_ordem[ordem]["linha"]["confiavel"] = True
					dict_ordem[ordem]["info"] = campos
				else:
					dict_ordem[ordem]["ultima_data"] = data
					dict_ordem[ordem]["pontos"].append([lat,lng])
					dict_ordem[ordem]["info"] = campos
					dict_ordem[ordem]["linha"]["num"] = linha_num
					dict_ordem[ordem]["linha"]["confiavel"] = True
					if len(dict_ordem[ordem]["pontos"]) > num_pontos: #lista de pontos atingiu o limite de pontos analisados
									dict_ordem[ordem]["pontos"].popleft()					
		finish = time.time()
		if finish - start < 60:
			time.sleep(60 - (finish - start))
		else:
			print "get_dados() demorou mais que 60 segundos"

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
		try:
			lng = float(ponto.split(" ")[0].split("(")[1])
			lat = float(ponto.split(" ")[1].split(")")[0])
			key = format(lat,'.'+n_dec+'f')+","+format(lng,'.'+n_dec+'f')
			if key in grid:
				grid[key].append((linha_num,lat,lng))
			else:
				grid[key] = []
		except:
			print linha_num

def carrega_grid():
	carrega_linha("422")
	carrega_linha("298")
	carrega_linha("864a")
	carrega_linha("864b")
	carrega_linha("326a")
	carrega_linha("326b")
	#carrega_linha("908b")
	#carrega_linha("908a")
	#carrega_linha("778b")
	#carrega_linha("778a")
	#carrega_linha("455a")
	#carrega_linha("455b")

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

##comeca servidor

app = web.application(urls, globals())

class get_linha:
	def GET(self, linha):
		with lock:
			if linha in dict_linha:
				ordens = dict_linha[linha]
				retorno = '{"COLUMNS":["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"],"DATA":['
				for ordem in ordens:
					if ordem in dict_ordem:
						campos = dict_ordem[ordem]["info"]
						retorno = retorno + '["' + campos[0] + '","' + campos[1]+ '",' + campos[2] + "," + campos[3].replace('"','') + "," + campos[4].replace('"','') + "," + campos[5][:-1] + ",0],"
					else:
						return "deu ruim na ordem "+ordem
				return retorno[:-1]+"]}"
			else:
				return "777 deu ruim"

class list_linhas:
	def GET(self):
		with lock:
			retorno = '{"COLUMNS":["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"],"DATA":['
			for ordem in dict_ordem:
				campos = dict_ordem[ordem]["info"]
				retorno = retorno + '["' + campos[0] + '","' + campos[1]+ '",' + campos[2] + "," + campos[3].replace('"','') + "," + campos[4].replace('"','') + "," + campos[5][:-1] + ",0],"
			return retorno[:-1]+"]}"

app.run()

#funcoes de teste

counter = 0
lista_ordens = []
with lock:
	for linha in dict_linha:
		lista = dict_linha[linha]		
		for ordem in lista:
			lista_ordens.append(ordem)

print counter

counter = 0
with lock:
	for ordem in dict_ordem:
		#if dict_ordem[ordem]["linha"]["confiavel"] == False and dict_ordem[ordem]["linha"]["num"] != '':
		if dict_ordem[ordem]["linha"]["num"] != '':
			counter+=1
			#if ordem not in lista_ordens:
			#	print ordem

print counter

#gravar posicoes em arquivo p teste
f = open("dict.txt","w")
f.write("chave;linha;latitude;longitude")
with lock:
	for chave in (ordem for ordem in dict_ordem if dict_ordem[ordem]["linha"]["confiavel"] == False and dict_ordem[ordem]["linha"]["num"] != ""):
		try:
			dados = dict_ordem[chave]["pontos"]
			for coord in dados:
				lati = str(coord[0])
				longi = str(coord[1])
				f.write(chave+";"+dict_ordem[chave]["linha"]+";"+lati + ";" + longi + "\n")
		except:
			print chave

f.close()

#gravar posicoes de uma so ordem
f = open("dict.txt","w")
ords = "A29005"
dados = dict_ordem[ords]["pontos"]
for coord in dados:
	lati = str(coord[0])
	longi = str(coord[1])
	f.write(lati + " " + longi + " ")
	print ords+";"+dict_ordem[ords]["linha"]["num"]+";"+lati + ";" + longi + ";"

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
