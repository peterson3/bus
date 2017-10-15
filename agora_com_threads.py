import sys
import gmplot
import urllib
import time
import os
from collections import deque
import threading
import math

dict = {} #guarda ultimas posicoes dos onibus ----> dict[ordem]["dados"/"ultima_data"]
dict_linhas = {} #guarda linhas descobertas ----> dict_linhas[ordem] = linha
grid = {} #guarda posicoes das trajetorias ja conhecidas ----> grid[key].append((linha_num,lat,lng))

lock = threading.RLock()

num_pontos = 5 #numero de pontos para olhar para tras

n_dec = '3' #numero de casas decimais da key

def distance_to_line(p,pr1,pr2):
	print "pontos"
	print p
	print pr1
	print pr2
	x_diff = pr2[0] - pr1[0]
	print "x dif"
	print x_diff
	y_diff = pr2[1] - pr1[1]
	print "y dif"
	print y_diff
	num = abs(y_diff*p[0] - x_diff*p[1] + pr2[0]*pr1[1] - pr2[1]*pr1[0])
	print "num"
	print num
	den = math.sqrt(y_diff**2 + x_diff**2)
	print "den"
	print den
	return num / den

def distance_to_point(p1,p2):
	return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

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
		urllib.urlretrieve ("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm", "onibus/bus.txt")
		fr = open("onibus/bus.txt")
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

def acha_linha_4(pontos):
	dict_d_linhas = {} # dicionario de possiveis melhores linhas
	pontuacao_maxima = 100 # pode diminuir caso nao haja nenhuma linha possivel na celula
	for ponto in pontos: #pontos por onde a ordem passou
		lat = ponto[0]
		lng = ponto[1]
		key = format(lat,'.'+n_dec+'f')+","+format(lng,'.'+n_dec+'f')
		print "key"
		print key
		if key in grid and len(grid[key]) > 0: # se existe alguma linha passando pela celula do ponto
			possibilidades = grid[key] # busca linhas que passam pela mesma celula que o ponto
			if len(possibilidades) == 0: # se nao ha linha possivel
				pontuacao_maxima -= 100/num_pontos
			print "possibilidades"
			print possibilidades
			linha_pontuacao = {} # guarda a pontuacao de uma linha e a distancia
			for i in range (0,len(possibilidades)):
				poss1 = possibilidades[i]
				print "poss1"
				print poss1
				poss1_linha = poss1[0]
				if poss1_linha not in linha_pontuacao:
					linha_pontuacao[poss1_linha] = {}
					linha_pontuacao[poss1_linha]["dist"] = 9999999999
				poss1_lat = poss1[1]
				poss1_lng = poss1[2]
				if len(possibilidades) > i + 1: # se eh possivel pegar um ponto a frente
					poss2 = possibilidades[i + 1]
					poss2_linha = poss2[0]
					if poss2_linha == poss1_linha and poss2 != poss1:
						print "ponto"
						print ponto
						print "poss2"
						print poss2
						dist = distance_to_line(ponto,[poss1_lat,poss1_lng],[poss2[1],poss2[2]]) # calcula a distancia entre o ponto e a linha formada pelas duas possibilidades
						if dist < linha_pontuacao[poss1_linha]["dist"]:
							linha_pontuacao[poss1_linha]["dist"] = dist
				else: # calcular distancia somente entre o ponto e a possibilidade
					dist = distance_to_point(ponto,[poss1_lat,poss1_lng])
					if dist < linha_pontuacao[poss1_linha]["dist"]:
							linha_pontuacao[poss1_linha]["dist"] = dist
			#calcula Req e v
			req_inv = 0
			print "linha_pontuacao"
			print linha_pontuacao
			for linha in linha_pontuacao:
				req_inv += 1/float(linha_pontuacao[linha]["dist"])
			print "req_inv"
			print req_inv
			req = 1/float(req_inv)
			print "req"
			print req
			v = req * 100
			#calcula pontuacao de cada linha
			for linha in linha_pontuacao:
				i = v/float(linha_pontuacao[linha]["dist"]) # i eh a pontuacao (max eh 100)
				if linha in dict_d_linhas:
					dict_d_linhas[linha] += i
				else:
					dict_d_linhas[linha] = i
		else: # se nao ha pontos na celula
			pontuacao_maxima -= 100/num_pontos
	# calcula soma da pontuacao de todas as linhas
	soma = 0
	for linha in dict_d_linhas:
		soma += dict_d_linhas[linha]
	# calcula pontuacao final de cada linha
	dict_final = {}
	for linha in dict_d_linhas:
		dict_final[linha] = dict_d_linhas[linha] * pontuacao_maxima / float(soma)
	dict_final[""] = 100 - pontuacao_maxima
	return dict_final

# retorna melhor linha a partir dos pontos por onde a ordem passou
def acha_linha_3(pontos):
	dict_d_linhas = {} # dicionario de possiveis melhores linhas
	counter_prob = 0
	for ponto in pontos: #pontos por onde a ordem passou
		lat = ponto[0]
		lng = ponto[1]
		key = format(lat,'.'+n_dec+'f')+","+format(lng,'.'+n_dec+'f')
		if key in grid: # se existe alguma linha passando pela celula do ponto
			possibilidades = grid[key] # busca linhas que passam pela mesma celula que o ponto
			for p_ponto in possibilidades:
				menor_dist = 99999999
				p_linha = p_ponto[0]
				p_lat = p_ponto[1]
				p_lng = p_ponto[2]
				for p2_ponto in (y for y in possibilidades if p_linha == p2_ponto[0] and p2_ponto[1] < p_lat): # comparando pares pontos de mesma linha, sem repeticao  
					p2_linha = p2_ponto[0]
					p2_lat = p2_ponto[1]
					p2_lng = p2_ponto[2]
					dist = distance_to_line(ponto,p_ponto,p2_ponto) ###########
					if dist < menor_dist:
						menor_dist = dist
				if p_linha not in dict_d_linhas: # se primeira vez que a linha aparece nessa busca
					dict_d_linhas[p_linha] = (d,1)
					counter_prob += 1
				else:
					counter_prob += 1
					for outro_ponto in dict_d_linhas:
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
	f = open("linhas/{linha_num}.csv".format(linha_num = linha_num))
	f.readline()
	for ponto in f:
		lng = float(ponto.split(" ")[0].split("(")[1])
		lat = float(ponto.split(" ")[1].split(")")[0])
		key = format(lat,'.'+n_dec+'f')+","+format(lng,'.'+n_dec+'f')
		if key in grid:
			grid[key].append((linha_num,lat,lng))
		else:
			grid[key] = [(linha_num,lat,lng)]

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
	f = open("bus/{linha_num}.csv".format(linha_num = linha))
	f.readline()
	for ponto in f:
		lng = ponto.split(" ")[0].split("(")[1]
		lat = ponto.split(" ")[1].split(")")[0]
		fw.write(linha+";"+linha+";"+lat+";"+lng+"\n")

fw.close()