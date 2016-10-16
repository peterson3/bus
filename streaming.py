from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext()

ssc = StreamingContext(sc, 1)

lines = ssc.textFileStream("/teste")

counts = lines.flatMap(lambda line: line.split(" "))\
              .map(lambda x: (x, 1))\
              .reduceByKey(lambda a, b: a+b)

counts.saveAsTextFile("/teste/teste")

ssc.start()
ssc.awaitTermination()