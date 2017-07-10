f_name = "C:/Users/IBM_ADMIN/Documents/tcc/testes/908-20p-2cd-20170709100747.txt"
f = open(f_name)

fw = open(f_name+"RESULTADOS","w")

pontuacao = 0
num_logs = 0
acertos = 0
erros = 0

elimina_pontuacao_vazia = False

for linha in f:
	linha = linha.replace("\n","")
	try: 
		if elimina_pontuacao_vazia:
			if float(linha) > 0:
				pontuacao += float(linha)
				num_logs += 1
			else:
				erros -=1
		else:
			pontuacao += float(linha)
			num_logs += 1
	except:
		if linha == "s":
			acertos += 1
		elif linha == "n":
			erros += 1
		else:
			print linha

fw.write("Numero de acertos: "+str(acertos)+"\n")
fw.write("Numero de erros: "+str(erros)+"\n")
fw.write("Proporcao de acertos: "+str(float(acertos)/(acertos+erros))+"\n")
fw.write("Pontuacao correta media: "+str(float(pontuacao)/num_logs)+"\n")

fw.close()
f.close()