import web
import variaveis
import json

class get_linha:
	def GET(self, linha):
		##teste
		with variaveis.lock:
			if linha in variaveis.dict_linha:
				ordens = variaveis.dict_linha[linha]
				retorno = {}
				retorno["DATA"] = []
				for ordem in ordens:
					if ordem in variaveis.dict_ordem:
						campos = variaveis.dict_ordem[ordem]["info"]
						itens = []
						itens.append(campos[0])
						itens.append(campos[1])
						try:
							itens.append(float(variaveis.dict_ordem[ordem]["linha"]["num"]))
						except:
							itens.append(variaveis.dict_ordem[ordem]["linha"]["num"])
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
		with variaveis.lock:
			if linha in variaveis.dict_linha:
				ordens = variaveis.dict_linha[linha]
				retorno = '{"COLUMNS":["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"],"DATA":['
				for ordem in ordens:
					if ordem in variaveis.dict_ordem:
						campos = variaveis.dict_ordem[ordem]["info"]
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
		with variaveis.lock:
			retorno["DATA"] = []
			for ordem in variaveis.dict_ordem:
				campos = variaveis.dict_ordem[ordem]["info"]
				itens = []
				itens.append(campos[0])
				itens.append(campos[1])
				try:
					itens.append(float(variaveis.dict_ordem[ordem]["linha"]["num"]))
				except:
					itens.append(variaveis.dict_ordem[ordem]["linha"]["num"])
				itens.append(float(campos[3].replace('"','')))
				itens.append(float(campos[4].replace('"','')))
				itens.append(float(campos[5][:-1]))
				itens.append(0)
				retorno["DATA"].append(itens)
		retorno["COLUMNS"] = ["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"]
		return json.dumps(retorno)
		with variaveis.lock:
			retorno = '{"COLUMNS":["DATAHORA","ORDEM","LINHA","LATITUDE","LONGITUDE","VELOCIDADE","DIRECAO"],"DATA":['
			for ordem in variaveis.dict_ordem:
				campos = variaveis.dict_ordem[ordem]["info"]
				retorno = retorno + '["' + campos[0] + '","' + campos[1]+ '",' + campos[2] + "," + campos[3].replace('"','') + "," + campos[4].replace('"','') + "," + campos[5][:-1] + ",0],"
			return retorno[:-1]+"]}"

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))
		
def comeca_server():
	#app = web.application(variaveis.urls, globals())
	app = MyApplication(variaveis.urls, globals())
	app.run(port=8888)