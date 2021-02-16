import numpy as np
from pyspark import SparkContext


sc = SparkContext(master="local[4]")

A = np.random.randint(0,10,20)

RDD_A = sc.parallelize(A)

print(RDD_A.collect())

print(RDD_A.glom().collect())

RDD_A_Distinct = RDD_A.distinct()

print(RDD_A_Distinct.collect())

print(RDD_A.sum())

print(RDD_A.reduce(lambda x,y:x+y))

print(RDD_A.fold(0,lambda x,y:x+y))

print(RDD_A.filter(lambda x:x%2==0 ).collect())

print(RDD_A.min(), RDD_A.max(), RDD_A.stdev(), RDD_A.stats())

RDD_B = RDD_A.map(lambda x:x*x )

print(RDD_B.collect())

def square_x(x):
   return x*x

RDD_B2 = RDD_A.map(square_x)

print(RDD_B2.collect())

C = np.random.randint(0,10,2)
RDD_C = sc.parallelize(C)
D = A = np.random.randint(0,10,3)
RDD_D = sc.parallelize(D)
print(RDD_C.collect())
print(RDD_D.collect())
print((RDD_C+RDD_D).collect())

print(RDD_C.cartesian(RDD_D).collect())

sc.stop()


