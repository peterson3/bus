import datetime
import threading

t_inicio = str(datetime.datetime.now()).split(".")[0].replace(":","").replace("-","").replace(" ","")

urls = ('/linhas', 'list_linhas','/linhas/(.*)', 'get_linha')

dict_ordem = {} #guarda info de ordens ----> dict_ordem[ordem]["pontos"/"ultima_data"/"linha"]
dict_linha = {} #guarda ordens relativas e uma linha ----> dict_linha[linha] = [ordens]
grid = {} #guarda posicoes das trajetorias ja conhecidas ----> grid[key].append((linha_num,lat,lng))

lock = threading.RLock()

num_pontos = 5 #numero de pontos para olhar para tras

n_dec = '3' #numero de casas decimais da key