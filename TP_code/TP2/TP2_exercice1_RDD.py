# Introduction sur les RDD
# import des librairies bumpy et py spark
import numpy as np
from pyspark import SparkContext

# Initialisation de Spark Context 4 partitions
sc = SparkContext(master="local[4]")

# Initialisation d'un vecteur de 20 nbre aléatoires (entierer)
A = np.random.randint(0,10,20)

# Creation d'un RDD parallelise a partir du vecteur précédent  
RDD_A = sc.parallelize(A)

# Affichage
print(RDD_A.collect())

# Affichage des partitions
print(RDD_A.glom().collect())

# Création d'un vecteur avec des valeurs uniques
RDD_A_Distinct = RDD_A.distinct()

# Affichage
print(RDD_A_Distinct.collect())

# Somme des valeur de RDD_A
# Utilisation de l fonction sum()
print(RDD_A.sum())

# utilisation de la fonction reduce avec appliquant une somme
print(RDD_A.reduce(lambda x,y:x+y))

# utilisation de fold
print(RDD_A.fold(0,lambda x,y:x+y))

# filtrer en ne retenant que les nbres pairs
print(RDD_A.filter(lambda x:x%2==0 ).collect())

# affichage du min, max, écart type, des stats
print(RDD_A.min(), RDD_A.max(), RDD_A.stdev(), RDD_A.stats())

# faire un map en mettant au carre
RDD_B = RDD_A.map(lambda x:x*x )

# afficher
print(RDD_B.collect())

# définir une fonction
def square_x(x):
   return x*x

# faire un map en appliquant une fonction
RDD_B2 = RDD_A.map(square_x)

#Affichage
print(RDD_B2.collect())

# créer 2 vecteurs aléatoires puis les RDD associés
C = np.random.randint(0,10,2)
RDD_C = sc.parallelize(C)
D = A = np.random.randint(0,10,3)
RDD_D = sc.parallelize(D)
print(RDD_C.collect())
print(RDD_D.collect())

# Fusionner les 2 RDD et afficher
print((RDD_C+RDD_D).collect())

# Former tous les couples possible (c_i, d_j)
print(RDD_C.cartesian(RDD_D).collect())

# on n'oublie d'arrêter le spark context
sc.stop()


