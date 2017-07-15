import sys
import urllib
import time
import os
import web
import json
#from PIL import Image
import math

from m_carrega_dados import *
from m_data_rio import *
from m_infere_linhas import *
from m_disponibiliza import *
from variaveis import *

carrega_grid()

threading.Thread(target = get_dados).start()
threading.Thread(target = t_encontrar_linhas).start()


