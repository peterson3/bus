import web

class get_linha:
	def GET(self, linha):
		##teste
		with lock:
			if linha in dict_linha:
				ordens = dict_linha[linha]
				retorno = {}
				retorno["DATA"] = []
				for ordem in ordens:
					if ordem in dict_ordem:
						campos = dict_ordem[ordem]["info"]
						itens = []
						itens.append(campos[0])
						itens.append(campos[1])
						try:
							itens.append(float(dict_ordem[ordem]["linha"]["num"]))
						except:
							itens.append(dict_ordem[ordem]["linha"]["num"])
						itens.append(float(campos[3].replace('"','')))
						itens.append(float(campos[4].replace('"','')))
						itens.append(float(campos[5][:-1]))
						itens.append(0)
						retorno["DATA"].append(itens)
					else:
						return "deu ruim na ordem "+ordem
			else:
				return '{"COLUMNS":["MENSAGEM"],"DATA":[["A requisicao foi processada corretamente, porem nenhum registro foi encontrado"]]}'
		retorno["COLUMNS"] = ["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"]
		return json.dumps(retorno)
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
				return '{"COLUMNS":["MENSAGEM"],"DATA":[["A requisicao foi processada corretamente, porem nenhum registro foi encontrado"]]}'

class list_linhas:
	def GET(self):
		##teste
		retorno = {}
		with lock:
			retorno["DATA"] = []
			for ordem in dict_ordem:
				campos = dict_ordem[ordem]["info"]
				itens = []
				itens.append(campos[0])
				itens.append(campos[1])
				try:
					itens.append(float(dict_ordem[ordem]["linha"]["num"]))
				except:
					itens.append(dict_ordem[ordem]["linha"]["num"])
				itens.append(float(campos[3].replace('"','')))
				itens.append(float(campos[4].replace('"','')))
				itens.append(float(campos[5][:-1]))
				itens.append(0)
				retorno["DATA"].append(itens)
		retorno["COLUMNS"] = ["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"]
		return json.dumps(retorno)
		with lock:
			retorno = '{"COLUMNS":["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"],"DATA":['
			for ordem in dict_ordem:
				campos = dict_ordem[ordem]["info"]
				retorno = retorno + '["' + campos[0] + '","' + campos[1]+ '",' + campos[2] + "," + campos[3].replace('"','') + "," + campos[4].replace('"','') + "," + campos[5][:-1] + ",0],"
			return retorno[:-1]+"]}"

def comeca_server():
	app = web.application(urls, globals())
	app.run()