import numpy as np
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


sc = SparkSession.builder.appName('TP1 part2').getOrCreate()

A = pd.DataFrame(np.random.randint(0,10,(20, 2)),columns=['A', 'B'])

RDD_A = sc.createDataFrame(A)
RDD_A.show()

RDD_B = RDD_A.withColumn('C', F.lit(0))
RDD_B.show()


RDD_C = RDD_A.withColumn('C', RDD_A.A - RDD_A.B)
RDD_C.show()

RDD_D = RDD_C.withColumn('D', df.C > 0)
RDD_D.show()

RDD_E = RDD_A.groupBy("A").agg(F.avg("B"), F.min("B"), F.max("B"))
RDD_E.show()

sc.stop()




