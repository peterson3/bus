import variaveis

def carrega_linha(linha_num):
	f = open("linhas/{linha_num}.csv".format(linha_num = linha_num))
	f.readline()
	for ponto in f:
		try:
			lng = float(ponto.split(" ")[0].split("(")[1])
			lat = float(ponto.split(" ")[1].split(")")[0])
			key = format(lat,'.'+variaveis.n_dec+'f')+","+format(lng,'.'+variaveis.n_dec+'f')
			if key in variaveis.grid:
				variaveis.grid[key].append((linha_num,lat,lng))
			else:
				variaveis.grid[key] = []
		except Exception,e:
			pass

def carrega_grid():
	carrega_linha("864a")
	"""
	carrega_linha("864")
	#carrega_linha("864b")
	carrega_linha("908")
	#carrega_linha("908a")
	carrega_linha("778")
	#carrega_linha("778a")
	carrega_linha("455")
	#carrega_linha("455b")
	carrega_linha("422")
	#carrega_linha("422b")
	carrega_linha("326")
	#carrega_linha("326b")
	carrega_linha("298")
"""
