import time
import urllib
import variaveis
from collections import deque
import datetime

def get_dados():
	while(True):
		start = time.time()
		urllib.urlretrieve ("http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/csv/onibus.cfm", "C:/Users/IBM_ADMIN/Documents/tcc/bus5.txt")
		fr = open("C:/Users/IBM_ADMIN/Documents/tcc/bus5.txt")
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
			#verifica se ponto eh agua. ignora ponto caso positivo. comentado por questoes de performance
			#if is_agua(str(lat),str(lng)):
			#	continue
			if linha_num == "": #linha nao informada
				with variaveis.lock:
					if ordem in variaveis.dict_ordem:
						if data != variaveis.dict_ordem[ordem]["ultima_data"]: #posicao eh nova
							#verifica se onibus se moveu
							inserir = True
							if(datetime.datetime.strptime(data, '%m-%d-%Y %H:%M:%S') < datetime.datetime.now() - datetime.timedelta(hours=3)):
								print datetime.datetime.strptime(data, '%m-%d-%Y %H:%M:%S')
								inserir = False
							for ponto in variaveis.dict_ordem[ordem]["pontos"]:
								if lat == ponto[0] and lng == ponto[1]:
									#print ponto
									inserir = False
							if inserir:
								#dict_ordem[ordem]["linha"]["num"] = ""
								variaveis.dict_ordem[ordem]["linha"]["confiavel"] = False 
								variaveis.dict_ordem[ordem]["pontos"].append([lat,lng])
								variaveis.dict_ordem[ordem]["ultima_data"] = data
								variaveis.dict_ordem[ordem]["info"] = campos
								if len(variaveis.dict_ordem[ordem]["pontos"]) > variaveis.num_pontos: #lista de pontos atingiu o limite de pontos analisados
									variaveis.dict_ordem[ordem]["pontos"].popleft()
					else:
						variaveis.dict_ordem[ordem] = {}
						variaveis.dict_ordem[ordem]["ultima_data"] = data
						variaveis.dict_ordem[ordem]["pontos"] = deque([[lat,lng]])
						variaveis.dict_ordem[ordem]["linha"] = {}
						variaveis.dict_ordem[ordem]["linha"]["num"] = ""
						variaveis.dict_ordem[ordem]["linha"]["confiavel"] = False
						variaveis.dict_ordem[ordem]["info"] = campos
			else: #if linha_num != '' se linha foi informada
				#tira ordem da linha anterior
				remove_ordem(ordem)
				#inclui ordem na nova linha
				if linha_num not in variaveis.dict_linha: #linha nao esta no dicionario
					variaveis.dict_linha[linha_num] = [ordem]
				else:
					variaveis.dict_linha[linha_num].append(ordem)
				#inclui/atualiza ordem no dict_ordem
				if ordem not in variaveis.dict_ordem: #ordem nao esta no dicionario
					variaveis.dict_ordem[ordem] = {}
					variaveis.dict_ordem[ordem]["ultima_data"] = data
					variaveis.dict_ordem[ordem]["pontos"] = deque([[lat,lng]])
					variaveis.dict_ordem[ordem]["linha"] = {}
					variaveis.dict_ordem[ordem]["linha"]["num"] = linha_num
					variaveis.dict_ordem[ordem]["linha"]["confiavel"] = True
					variaveis.dict_ordem[ordem]["info"] = campos
				else:
					variaveis.dict_ordem[ordem]["ultima_data"] = data
					variaveis.dict_ordem[ordem]["pontos"].append([lat,lng])
					variaveis.dict_ordem[ordem]["info"] = campos
					variaveis.dict_ordem[ordem]["linha"]["num"] = linha_num
					variaveis.dict_ordem[ordem]["linha"]["confiavel"] = True
					if len(variaveis.dict_ordem[ordem]["pontos"]) > variaveis.num_pontos: #lista de pontos atingiu o limite de pontos analisados
									variaveis.dict_ordem[ordem]["pontos"].popleft()					
		finish = time.time()
		if finish - start < 60:
			time.sleep(60 - (finish - start))
		else:
			print "get_dados() demorou mais que 60 segundos"

def remove_ordem(ordem): #remove ordem do dict_linha
	counter = 0
	for linha in variaveis.dict_linha:
		if ordem in variaveis.dict_linha[linha]:
			variaveis.dict_linha[linha].remove(ordem)
			counter += 1
	if counter > 1:
		print "removidas {n} ocorrencias da ordem {ordem}. Isso nao devia ter acontecido".format(n = counter, ordem = ordem)

