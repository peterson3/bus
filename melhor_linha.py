from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, HiveContext, Row
from pyspark.sql.types import *  
import sys
import gmplot
import sys
from pyspark.sql.window import Window
import pyspark.sql.functions as func

conf = SparkConf()

#conf.setMaster("yarn-client")

sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)

sqlContext.setConf("hive.exec.dynamic.partition.mode", "nonstrict")

bus = sqlContext.read.json("file:///home/Natalia/json")

bus.registerTempTable("bus")

rdd = sqlContext.sql("select t from bus lateral view explode(data) a as t").map(lambda x: Row(data = x[0][0],ordem = x[0][1],linha = \
    x[0][2],lat = x[0][3], lon = x[0][4], velocidade = x[0][5])).cache()

df = sqlContext.createDataFrame(rdd)

flt = df.filter("ordem = 'D86387'")

#pega possiveis rotas

rot = sc.textFile("file:///home/Natalia/tcc/rota.csv")

rflt = rot.filter(lambda x: len(x) > 11) #elimina header

rmp = rflt.map(lambda x: ("864",(float(x.split(" ")[1].split(")")[0]),float(x.split(" ")[0].split("(")[1])))).cache()

rgrp = rmp.groupByKey()
    
rota_array = rgrp.map(lambda x : (x[0],list(x[1])))

cart = flt.rdd.cartesian(rota_array)

def teste(a):
    dados = a[0]
    lat = dados.lat
    ordem = dados.ordem
    lon = dados.lon
    linha = a[1][0]
    pontos = a[1][1]
    min_d = 9999999
    for ponto in pontos:
        d_lat = abs(float(lat) - ponto[0])
        d_lon = abs(float(lon) - ponto[1])
        d = d_lat + d_lon
        if(d < min_d):
            min_d = d
    return ((ordem,linha),min_d)

cart_map = cart.map(teste)

cart_test = cart_map.aggregateByKey((0,0), lambda a,b: (a[0] + b,    a[1] + 1),lambda a,b: (a[0] + b[0], a[1] + b[1]))

linhas_medias = cart_test.map(lambda v: Row(ordem = v[0][0],linha = v[0][1],media = v[1][0]/v[1][1]))

linhas_medias_df = sqlContext.createDataFrame(linhas_medias)

linhas_medias_df.registerTempTable("linhas_medias_df")

windowSpec =  Window.partitionBy(linhas_medias_df['ordem']).orderBy(linhas_medias_df['media'].desc()).rangeBetween(-sys.maxsize, sys.maxsize)

sl = (func.min(linhas_medias_df['media']).over(windowSpec))

linhas_medias_df.select(linhas_medias_df['ordem'],linhas_medias_df['linha'],sl.alias("media")).take(1)

##########

melhor_linha = sqlContext.sql("select ordem,linha,min(media) as media from linhas_medias_df group by ordem")

def soma(a,b):
    return a + b

cart_red = cart_map.reduceByKey(soma)

cart_med = 

cart_df = sqlContext.createDataFrame(cart)


#grp = rmp.groupByKey()

def minimo(a,b):
    return (min(a[0],b[0]),min(a[1],b[1]))

def maximo(a,b):
    return (max(a[0],b[0]),max(a[1],b[1]))

mins = rmp.reduceByKey(minimo)

maxs = rmp.reduceByKey(maximo)

uni = mins.union(maxs)

centroides = uni.reduceByKey(lambda a,b: ((a[0]+b[0])/2,((a[1]+b[1])/2)))