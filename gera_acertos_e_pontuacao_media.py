for linha_nome in ["326","422","455","778","864","908"]:
	f_name = "C:/Users/IBM_ADMIN/Documents/tcc/testes/testes_finais/{l}-10p-3cd-20170710093227.txt".format(l=linha_nome)
	f = open(f_name)
	
	fw = open(f_name+"RESULTADOS_LIMPOS","w")
	
	pontuacao = 0
	num_logs = 0
	acertos = 0
	erros = 0
	
	elimina_pontuacao_vazia = True
	
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