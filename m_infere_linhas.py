import time
import variaveis

def distance_to_line(p,pr1,pr2):
	#print "pontos"
	#print p
	#print pr1
	#print pr2
	x_diff = pr2[0] - pr1[0]
	#print "x dif"
	#print x_diff
	y_diff = pr2[1] - pr1[1]
	#print "y dif"
	#print y_diff
	num = abs(y_diff*p[0] - x_diff*p[1] + pr2[0]*pr1[1] - pr2[1]*pr1[0])
	#print "num"
	#print num
	den = math.sqrt(y_diff**2 + x_diff**2)
	#print "den"
	#print den
	return num / den

def distance_to_point(p1,p2):
	return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def acha_linha_4(pontos):
	dict_d_linhas = {} # dicionario de possiveis melhores linhas
	pontuacao_maxima = 100 # pode diminuir caso nao haja nenhuma linha possivel na celula
	for ponto in pontos: #pontos por onde a ordem passou
		lat = ponto[0]
		lng = ponto[1]
		key = format(lat,'.'+variaveis.n_dec+'f')+","+format(lng,'.'+variaveis.n_dec+'f')
		#print "key"
		#print key
		if key in variaveis.grid and len(variaveis.grid[key]) > 0: # se existe alguma linha passando pela celula do ponto
			possibilidades = variaveis.grid[key] # busca linhas que passam pela mesma celula que o ponto
			if len(possibilidades) == 0: # se nao ha linha possivel
				pontuacao_maxima -= 100/variaveis.num_pontos
			#print "possibilidades"
			#print possibilidades
			linha_pontuacao = {} # guarda a pontuacao de uma linha e a distancia
			for i in range (0,len(possibilidades)):
				poss1 = possibilidades[i]
				#print "poss1"
				#print poss1
				poss1_linha = poss1[0]
				if poss1_linha not in linha_pontuacao:
					linha_pontuacao[poss1_linha] = {}
					linha_pontuacao[poss1_linha]["dist"] = 9999999999
				poss1_lat = poss1[1]
				poss1_lng = poss1[2]
				soUmPonto = True # se so um ponto deve ser analisado
				if len(possibilidades) > i + 1: # se eh possivel olhar um ponto a frente
					poss2 = possibilidades[i + 1]
					poss2_linha = poss2[0]
					if poss2_linha == poss1_linha and poss2 != poss1: # se ponto seguinte pertence a mesma linha
						soUmPonto = False
						#print "ponto"
						#print ponto
						#print "poss2"
						#print poss2
						dist = distance_to_line(ponto,[poss1_lat,poss1_lng],[poss2[1],poss2[2]]) # calcula a distancia entre o ponto e a linha formada pelas duas possibilidades
						if dist == 0 : dist = 2.2250738585072014e-308 # min float (evita divisoes por 0)
						if dist < linha_pontuacao[poss1_linha]["dist"]:
							linha_pontuacao[poss1_linha]["dist"] = dist
				if soUmPonto: 
					# calcular distancia somente entre o ponto e a possibilidade
					dist = distance_to_point(ponto,[poss1_lat,poss1_lng])
					if dist == 0 : dist = 2.2250738585072014e-308 # min float (evita divisoes por 0)
					if dist < linha_pontuacao[poss1_linha]["dist"]:
							linha_pontuacao[poss1_linha]["dist"] = dist
							#print "dist " + poss1_linha + ": " + str(dist)
					else:
						pass
						#print "dist"
						#print poss1_linha + ": " + str(dist) + " >= " + str(linha_pontuacao[poss1_linha]["dist"])
			#calcula Req e v
			req_inv = 0
			#print "linha_pontuacao"
			#print linha_pontuacao
			for linha in linha_pontuacao:
				req_inv += 1/float(linha_pontuacao[linha]["dist"])
			#print "req_inv"
			#print req_inv
			req = 1/float(req_inv)
			#print "req"
			#print req
			v = req * 100
			#calcula pontuacao de cada linha
			for linha in linha_pontuacao:
				i = v/float(linha_pontuacao[linha]["dist"]) # i eh a pontuacao (max eh 100)
				if linha in dict_d_linhas:
					dict_d_linhas[linha] += i
				else:
					dict_d_linhas[linha] = i
		else: # se nao ha pontos na celula
			pontuacao_maxima -= 100/variaveis.num_pontos
	# calcula soma da pontuacao de todas as linhas
	soma = 0
	for linha in dict_d_linhas:
		soma += dict_d_linhas[linha]
	# calcula pontuacao final de cada linha
	dict_final = {}
	maior_pontuacao = 0
	linha_maior_pontuacao = ""
	for linha in dict_d_linhas:
		pontuacao = dict_d_linhas[linha] * pontuacao_maxima / float(soma)
		dict_final[linha] = pontuacao
		if pontuacao > maior_pontuacao:
			maior_pontuacao = pontuacao
			linha_maior_pontuacao = linha
	dict_final[""] = 100 - pontuacao_maxima
	if maior_pontuacao > 100 - pontuacao_maxima: # se alguma linha recebeu pontuacao maior que a linha vazia
		return linha_maior_pontuacao
	return ""
	#return dict_final


def encontrar_linhas():
	with variaveis.lock:
		for ordem in (ordem for ordem in variaveis.dict_ordem if variaveis.dict_ordem[ordem]["linha"]["confiavel"] == False):
				#se numero de pontos condiz com o necessario p/ analise
				if len(variaveis.dict_ordem[ordem]["pontos"]) == variaveis.num_pontos:
					linha = acha_linha_4(variaveis.dict_ordem[ordem]["pontos"],variaveis.n_dec)
					if linha != "":
						print "ordem {ordem} pertence a linha {linha}".format(ordem = ordem, linha = linha)
						#verifica se linha mudou p/ atualizar dicionarios
						if ordem in variaveis.dict_ordem:
							linha_antiga = variaveis.dict_ordem[ordem]["linha"]["num"]
							print linha_antiga + " linha antiga, linha nova: " + linha
							if linha_antiga != linha:	
								variaveis.dict_ordem[ordem]["linha"]["num"] = linha
								variaveis.dict_ordem[ordem]["linha"]["confiavel"] = False
								if linha_antiga != '':
									variaveis.dict_linha[linha_antiga].remove(ordem)
						else:
							print "ordem {ordem} nao estava no dicionario".format(ordem = ordem)
						if linha in variaveis.dict_linha:
							if ordem not in variaveis.dict_linha[linha]:
								variaveis.dict_linha[linha].append(ordem)
						else:
							variaveis.dict_linha[linha] = [ordem]


def t_encontrar_linhas():
	while True:
		start = time.time()
		encontrar_linhas()
		finish = time.time()
		if finish - start < 60:
			time.sleep(60 - (finish - start))
		else:
			print "encontrar linhas demorou mais que 60 segundos"
