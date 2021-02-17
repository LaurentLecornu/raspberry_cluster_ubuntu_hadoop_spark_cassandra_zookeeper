# **TP 2 : Exécution de Spark – Mode cluster – Exercices sur Spark**


# 1	Objectif

* Déploiement d’un cluster Spark
* Test de spark en mode cluster et écoute des ports
* Récupération du flux de données en streaming dans Spark
	* Intégration d’un flux de données


# 2	SPARK

## 2.1	Déploiement d’un cluster Spark

Un cluster Spark se compose d’un nœud master et plusieurs nœuds workers. Le master s’occupe uniquement de la gestion du cluster et les workers sont les exécuteurs des jobs MapReduce pour le traitement distribué.

Spark peut être utilisé seul. Il existe plusieurs méthodes pour le déployer. 

* Standalone Deploy Mode : la méthode la plus simple
* Apache Mesos
* Hadoop YARN : celle que l’on utilisera
* Kubernetes

Pour exécuter un traitement sur un cluster Spark, il faut soumettre une application dont le traitement sera piloté par un driver. Comme vous l’avez vu précédemment, deux modes d’exécution sont possibles :

* mode client : le driver est créé sur la machine qui soumet l’application
* mode cluster : le driver est créé à l’intérieur du cluster

Nous venons d’installer un cluster hadoop et d’utiliser yarn que nous allons utiliser pour spark. 


### 2.1.1	Installation de Spark sur tous les nœuds du cluster

La première étape est de vérifier que Spark sur chacun des nœuds de votre cluster.

	pi@pi-node29:~$ cd /opt/
	pi@pi-node29:~$ ls -l

On vérifie la version de spark et que le owner est pi.

	pi@pi-node29:~$ sudo chown -R pi:pi /opt/spark


A date la version de Spark est la 3.0.1, vous pouvez choisir une version plus récente si vous le souhaitez.

	pi@pi-node29:~$ wget https://downloads.apache.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz
	pi@pi-node29:~$ sudo tar -xvf spark-3.0.1-bin-hadoop3.2.tgz  -C /opt/

On peut soit modifier le nom du répertoire, soit mettre un lien symbolique. Voici les commandes utilisées.

	pi@pi-node29:~$ cd /opt/
	pi@pi-node29:~$ sudo mv spark-3.0.1-bin-hadoop3.2 spark
	pi@pi-node29:~$ sudo chown -R pi:pi /opt/spark


### 2.1.2	Configuration des fichiers
 
* Configuration du fichier : `~/.bashrc` 

Ajouter les lignes suivantes :

	export SPARK_HOME=/opt/spark
	export PATH=$PATH:$SPARK_HOME/bin

et

	export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
	export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH

* Configuration du fichier spark-defaults.conf

Le fichier `spark-defaults.conf` sera créé et modifié comme suit :

	$ cd /opt/spark/conf
	$ sudo mv spark-defaults.conf.template spark-defaults.conf
	$ nano spark-defaults.conf

Puis modifier le fichier comme suit : 

	spark.master            yarn
	spark.driver.memory     1136m
	spark.yarn.am.memory    512m
	spark.executor.memory   512m
	spark.executor.cores    2

Ici, on choisit d’utiliser `yarn`. Vous pouvez choisir de rester en mode local.

Attention : spark.driver.memory + 384 < yarn.nodemanager.resource.memory-mb 

(sinon spark ne pourra pas démarrer)

## 2.2	Test et observation du cluster

### 2.2.1	Test

Dans un premier temps, on stoppe et on redémarre hdfs et yarn

	$ start-dfs.sh
	$ start-yarn.sh

* Vérifier avec jps le bon démarrage du cluster hadoop.

Tester votre cluster en utilisant les programmes de tests présents avec spark.

	$ spark-submit --deploy-mode cluster –class org.apache.spark.examples.SparkPi /opt/spark/examples/jars/spark-examples_2.11-3.0.1.jar 7
		
Ou bien avec un fichier python

	$ spark-submit --deploy-mode cluster /opt/spark/examples/src/main/python/pi.py 10

(Il est possible de ne pas utiliser yarn)


### 2.2.2	Observation du cluster

Il suffit d’observer le bon port (en mode client) port 4040 (attention ce port n’est actif que lors de l’exécution du processus spark). 

Et les port 8088 et 9870 en mode cluster (c’est les mêmes qu’avec hadoop) qui permet d’observer le comportement du cluster yarn.


### 2.2.3	Création et test de son propre fichier spark

Dans un premier temps, arrêter le serveur yarn et dfs et utiliser spark sur un seul nœud. Cela va permettre de faire des tests plus rapidement.

	$ stop-yarn.sh
	$ stop-dfs.sh
	$ sudo mv spark-defaults.conf spark-defaults_1.conf




Ou bien modifier (il ne faudra oublier de la remplacer au cours de l’exercice 2)

	spark.master yarn

par :

    spark.master local[*]


#### Exercice 1 :

Créer et Compléter : `TP2_exercice1_part1.py`

Puis le soumettre :

	$ spark-submit TP2_exercice1_part1.py

(on prend les valeurs par défaut en local)

(vous modifier votre programme en fonction des questions rencontrées, attention les opération doivent être appliquées à des RDD ou des Dataframe (spark) et non des Dataframe (numpy))


-	Étude des RDD

	-	Utilisation de SparkContext de pyspark


	-	Créer un RDD composé de 20 nombres entiers aléatoires compris entre 0 et 9 inclus. 

		-	Utiliser numpy pour générer les nombres aléatoires puis créer un RDD
			-	`A = np.random.randint(deb_int.,fin_int.,nb_elts)`

		-	Lancer sc avec :
			-	`sc = SparkContext(master= "local[nbre_de_cœurs]")`
			-	remplacer `nbre_de_cœurs` par un nombre entier compris entre 1 et 4.
		-	A la fin du programme, n’oubliez pas d’arrêter le SparkContext en utilisant la fonction `stop()` de SparkContext avec :	
		
 	 			sc.stop()

		-	On commencera avec un nbre de cœurs égale à 2 puis on modifiera sa valeur (1 et 4)

			-	Créer un RDD nommé RDD_A à partir A :
				-	Utilisation de la commande parallelize de SparkContext qui sera appliqué à A et donnant comme résultat nommé : RDD_A
				-	Pour observer un RDD, on utilise la commande `collect()` qui récupère l’ensemble du contenu du rdd (à n’effectuer que lorsqu’on à besoin de tout récupérer)
					-	`type_rdd.collect()`
				-	Pour observer l’effet de la parallélisation (c’est-à-dire le contenu du RDD sur chaque cœur), on intercale la fonction glom() avant collect()
					-	observation : `type_rdd.glom().collect()`
			-	Un `print()` appliqué au contenu collecté affiche le résultat.

		-	Compter le nombre d’éléments
			-	Appliqué la fonction count() au RDD et affiché le résultat.

		-	Afficher la liste des entiers de la suite générée
			-	On applique la fonction `distinct()` à RRD_A et on sauve le résultat dans RDD_A_Distinct
			-	Afficher le résultat

		-	Indiquer la somme de ces 20 entiers. Il existe différentes façon de le faire, il suffit d’appliquer l’une des 3 fonctions suivantes au RDD. 
			-	sum()
			-	reduce(lambda x,y :x+y)
			-	fold(0, lambda x,y :x+y)
			-	A-t-on le même résultat ?
			-	Quelle est la différence entre reduce et fold ?

		-	Afficher les nombres pairs en appliquant la fonction filter au RDD 
			-	Nb : lambda x :x%2==0 dans filter peut aider

		-	Afficher quelques statistiques descriptives sur cette suite
			-	Appliquer max(), min(), stdev(), stats() à RDD_A puis afficher les résulats

		-	Mettre au carré RDD_A en lui appliquant un map
			-	Intégrer lambda x:x*x à l’intérieur du map puis récupérer le résultat dans RDD_B
			-	Créer une fonction qui est intégrer dans le map
				-	`def square_x(x):`
				
   					`return x*x`	

		-	type_rdd.map(square_x)
			-	Collecter puis afficher les résultats
			-	Quelles sont les différence entre map et flapmap

		-	Appliquer des opérations sur 2 suites aléatoires (RDD_C et RDD_D)
			-	La 1ère suite contient 3 nombres entiers (aléatoire) et la deuxième 4
			-	En effectuant l’union
				-	Faire « + » et collecter puis afficher le résultat
			-	Créer tous les couples (ci,dj) où ci (resp. dj) où représente ci l’ensemble des éléments de RDD_C (resp. de RDD_D)
				-	utiliser la fonction cartesian de RDD_C que l’on appliquera à RDD_D
				-	collecter puis afficher le résultat

Créer et compléter : `TP2_exercice1_part2.py`

Puis le soumettre :

	 $ spark-submit TP2_exercice1_part2.py

-	Étude DataFrame

	-	Nous allons d’abord créer un dataframe (grâce à panda) qui sera transformé en dataframe (spark). Puis on appliquera quelques opérations sur ce dataframe
	-	Petites modification dans les import
		-	import numpy as np
		-	import pandas as pd
		-	from pyspark.sql import SparkSession
		-	from pyspark.sql import functions as F
			-	functions regroupe des fonctions élémentaires tel que min(.), max(.)
	-	La session sc sera créée par :
		-	sc = SparkSession.builder.appName('TP1 part2').getOrCreate()
		-	Du fait d’un dataframe, on utilise pyspark.sql.
	-	Opérations simples appliquées sur un dataframe
		-	Création d’un dataframe (panda) nommé A comportant 2 colonnes (nommés A et B) et 20 lignes. On utilisera la fonction DataFrame de panda. Dans cette fonction, on intègrera une matrice (20,2) comportant un nombre aléatoire compris entre 0 et 9 (on utilisera la même fonction que précédemment).
		-	Création d’un dataframe nommé RDD_A en utilisant la fonction createDataFrame appliqué à A.
		-	Afficher le RDD_A en utilisant show()
		-	Créer un dataframe RDD_B contenant RDD_A et incluant une colonne C ne contenant que des 0
			-	Appliquer withColumn à RDD_A en créant une colonne ‘C’ initialisé par F.lit(0)
		-	Afficher le résultat
	-	Créer un dataframe RDD_C contenant RDD_A et incluant une colonne C contient les résultats de A-B
		-	De nouveau utiliser withColumn
	-	Créer un dataframe RDD_D contenant RDD_C et incluant une colonne D qui indique si la valeur de C est négative
	-	Créer un dataframe RDD_E en effectuant une aggrégation (groupBy) sur RDD_A des valeurs de A en affichant la moyenne (F.avg("B")) des valeurs de B (qui ont été aggrégées pour la valeur de A) ainsi que le mininum (F.min("B")), le maximum (F.max("B")) (ce qui doit donner un tableau comportant 10 lignes (0 à 9) et 4 colonnes (A, moyenne de B, minimum de B et maximum de B) 

	-	Synthétiser rapidement les différences entre un RDD et un Dataframe (en spark)

PS : Attention : La notion de dataframe existe également sous python


#### Exercice 2 : 

Étude de 2 textes en anglais : Frankeinstein of the Modern Prometheus et The Adventures of Sherlok Holmes

On commencera par démarrer les services dfs puis on copiera deux fichiers qui seront traités. On créera et completera TP2_exercice2.py

	$ start-dfs.sh
	$ hadoop fs -put /home/pi/holmes.txt /holmes.txt
	$ hadoop fs -put /home/pi/frankenstein.txt /frankenstein.txt

Puis le soumettre :

	$ spark-submit TP2_exercice2.py

-	Utiliser la fonction SparkContext de pyspark pour créer sc

-	Copier les fichiers (holmes.txt et frankenstein.txt) dans le répertoire hdfs en utilisant la commande hadoc.
-	Utiliser spark pour : 
	-	Lire les fichiers
		-	Utiliser la fonction textFile de sc que vous appliquerez à holmes.txt et frankenstein.txt permettant de créer 2 RDD text_file1 et text_file2
		-	Afficher les 3 premiers éléments de text_file1 ou 2 en utilisant la fonction take(3) de rdd (et print)
		-	Que contient chaque élément du rdd text_file1
	-	Déterminer le nombre d’occurrence de chaque mot et le nombre de mots (pour chaque fichier)
		-	Créer un rdd qui contient dans chaque élément un seul mot 
		-	Utiliser flatMap(lambda line : line.split(" "))
	-	Le séparateur de mot est 1 espace
		-	Filtrer le RDD afin d’enlever les mots vides ou autres à l’aide de la fonction filter du rdd précédent
	-	Compter le nombre de mots
	-	Créer un RDD de couple (mot,1) à l’aide de la fonction map du rdd de la ligne précédente
	-	Réduire par clefs en sommant les valeurs 
		-	Utilisation de la fonction reduceByKeys(lambda a,b : a+b)

-	Déterminer les probabilités d’apparition de chaque mot (pour chaque fichiers) on utilisera la fonction map and co.
-	Afficher les 10 mots les plus fréquents (occurrences et fréquences) pour chaque fichier
	-	Analyser le résultat
-	Comment étudier la différence entre les 2 textes 
-	Question philosophique : Est-ce que tous les mots ont la même importance ?

 
# 3	Test de la librairie SparkStreaming

## 3.1	Exemple de streaming

#### 3.1.1	Création d’un flux (socket) et ouverture d’un port

-	Ouvrir un flux
	-	Ouvrir un socket sur le port 9999 en utilisant netcat dans un terminal

			$ nc -l -p 9999

-	Vérifier si le port est ouvert et que le socket fonctionne
	-	Ouvrez un socket sur le port 9999 en utilisant netcat sur un deuxième terminal

			$ nc pi-nodeXXX 9999

(remplacer pi-nodeXXX par votre nœud)

-	Puis en tapant des mots sur le premier terminal. Ils apparaitront sur le deuxième.

L’annexe 1 indique comment envoyer en continu la date (toutes les 3 secondes sur netcat) par le biais d’une création de fichier.


### 3.1.2	Utilisation de Spark Streaming

Maintenant que les communications sont établies, il est préférable que Spark ce charge de traiter ce flux. C’est le rôle de Spark Streaming.

`https://spark.apache.org/docs/latest/api/python/pyspark.streaming.html`

Ici, nous allons juste compter le nombre d’erreurs qui se produisent

Nous allons commencer par créer et compléter : premierStreamApp.py

-	Pouvez-vous préciser le rôle des fonctions en gras ?

On crée :
* 	Un contexte spark
* 	Un contexte spark streaming
* 	On récupère le texte du flux émis
* 	On compte les mots
* 	On affiche le comptage
* 	On fait varier l’intervalle d’écoute

#### 3.1.2.1	Exemple 1 : Suite d’intervalles

Dans cet exemple, on va introduire les fonctionnalités de base :

* StreamingContext : permet d’établir une lecture d’un flux par intervalle de n secondes (ici 10)
* socketTextStream : permet de récupérer les données lues dans l’intrervalle
* pprint : affiche en flux

* `ssc.start()` : démarre le traitement 
* `ssc.awaitTermination()` : attend l’arrêt


Veuillez créer et compléter le fichier SparkStreamingEx3_part1.py :

	# Import libs

	from __future__ import print_function

	import sys

	from pyspark import SparkContext
	from pyspark.streaming import StreamingContext

	# Begin
	if __name__ == "__main__":
    	if len(sys.argv) != 3:
    	print("Usage: firstStreamApp.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    	sc = SparkContext(appName="SparkStreamingExercice3"); 

    	# 10 la duree de l’interval : 10 secondes
    	ssc = StreamingContext(à compléter)


    	# Lines n’est pas un rdd mais une suite de rdd, not statique, changeant constamment 

    	lines = à complèter.socketTextStream(sys.argv[1],\
              	int(sys.argv[2]),StorageLevel.MEMORY_AND_DISK)
    	# Que sont les valeurs de sys.argv[1] et sys.argv[2]
    	# Comptage
    	counts = lines.flatMap(à compléter)\
                  .map(à compléter)\
                  .reduceByKey(à compléter)
    # print en streaming
    counts.pprint()

    ssc.start() 
    ssc.awaitTermination()

 
Soumettez le script python
Ouvrez un socket sur le port 9999 en utilisant netcat sur ce deuxième terminal

	$ spark-submit SparkStreamingEx3_part1.py pi-nodeXXX 9999

(warning le démarrage sous yarn prend un peu de temps) 

Vous verrez apparaître les time slots

	$ spark-submit SparkStreamingEx3_part1.py pi-node29 9999
	17/04/12 10:38:15 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable 
	-------------------------------------------
	Time: 2017-04-12 10:38:18 
	-------------------------------------------
	-------------------------------------------
	Time: 2017-04-12 10:38:20 
	-------------------------------------------
	-------------------------------------------
	Time: 2017-04-12 10:38:22 
	-------------------------------------------
	-------------------------------------------
	Time: 2017-04-12 10:38:24 
	-------------------------------------------
	-------------------------------------------
	Time: 2017-04-12 10:38:26 
	-------------------------------------------
	-------------------------------------------
	Time: 2017-04-12 10:38:28 
	-------------------------------------------

Le résultat obtenu n’est pas aussi joli. En effet, Spark peut afficher trop d’INFO.

Le résultat du programme Spark Driver est riche en log de type INFO, ce qui peut obscurcir les résultats. Une stratégie possible est de changer le niveau de logs Spark vers WARN, en modifiant le fichier “spark/conf/log4j.properties” (si des problèmes apparaissent, il vaudra mieux revenir au niveau de logs INFO).
Cela va rendre Spark moins verbeux.

	#Set Spark's console output log level to WARN
	$ cp /opt/spark/conf/log4j.properties.template /opt/spark/conf/log4j.properties

Puis modifier la ligne : log4j.rootCategory=INFO, console
Par : log4j.rootCategory=WARN, console


#### 	3.1.2.2	Exemple 2 : Intégration sur plusieurs intervalles

Le résultat précédent ne traite que l’intervalle. Ici, nous allons intégrer les calculs sur plusieurs intervalles


On étudiera la fonction : UpdateStateByKey

Veuillez créer et compléter le fichier : SparkStreamingEx3_part2.py

	import sys
	from pyspark import SparkContext
	from pyspark.streaming import StreamingContext

	if __name__ == "__main__":
    	sc = SparkContext(appName="Exercice3part2"); 
    	# 2 is the batch interval : 2 seconds
    	ssc = StreamingContext(à compléter)
    	# Checkpoint for backups

    	lines = ssc.socketTextStream(à compléter)

	    # Update function
    	def countWords(newValues, lastSum): 
       	 if lastSum is None :
            lastSum = 0
        return sum(newValues, lastSum)

    	word_counts = lines.flatMap(lambda line: line.split(" "))\ 
        .map(lambda word : (word, 1))\
        .updateStateByKey(countWords)

    	word_counts.pprint() 
    	ssc.start() 
    	ssc.awaitTermination()


Analyser le rôle des nouvelles fonctions, c’est-à-dire pourriez-vous expliquez :
-	La fonction countWords (décrire l’algorithme suivi)
-	updateStateByKey(.)


Lancez netcat comme précédemment

	$ nc -l -p 9999

• Soumettre le script python

Open a socket on port 9999 using netcat

	$ spark-submit ??.py pi-nodeXXX 9999

#### 3.1.2.3	Exemple 3 : Utilisation d’une fenêtre glissante

On étudiera la fonction  : countByWindow

Veuillez créer et compléter le fichier : SparkStreamingEx3_part3.py

	# Import libs
	import sys
	from pyspark import SparkContext
	from pyspark.streaming import StreamingContext

	if __name__ == "__main__":
    	sc = SparkContext(appName="Exercice2"); 
    	# 2 is the batch interval : 10 seconds
    	ssc = StreamingContext(à compléter)



    	lines = à compléter.socketTextStream(à compléter)
    
    	## taille de la fenêtre = 10, 
    	## intervalle glissant = 2
    	counts = à completer countByWindow(à compléter)

	    ## Affichage
    	counts.pprint()
    	ssc.start()
    	ssc.awaitTermination()

Pourriez-vous expliquez :
-	countByWindow(.)

	$ nc -l -p 9999

Soumettre le script

	$ spark-submit ??.py localhost 9999

#### 3.1.2.4	Exemple 4

Étude de la fonction suivante : reduceByWindow

Veuillez créer et compléter le fichier : SparkStreamingEx3_part4.py

	# Import libs
	import sys
	from pyspark import SparkContext
	from pyspark.streaming import StreamingContext

	if __name__ == "__main__":
    sc = SparkContext(appName="StreamingreduceByWindow"); 
    # intervalle : 2 secondes
    ssc = StreamingContext(à compléter)

    lines = à completer .socketTextStream(à compléter)

    ## summary function
    ## reverse function
    ## window size = 10
    ## sliding interval = 2 
    sum = lines.reduceByWindow(
        lambda x, y: int(x) + int(y), 
        lambda x, y: int(x) - int(y), 
        10,
        2
    )

    ## Affichage
    sum.pprint()
    ssc.start()
    ssc.awaitTermination()

Pourriez-vous expliquez :

-	reduceByWindow(.)
-	Comparer reduceByWindow et counByWindow, indiquer les différences
-	Est-il possible de connaître les entrants et les sortants de l’intervalle (suite au glissement de l’intervalle)

		$ spark-submit ???.py localhost 9999


#### 3.1.2.5	Exemple 5 :

 Étude de la fonction : reduceByKeyAndWindow

Veuillez créer et compléter le fichier : SparkStreamingEx3_part5.py

	# Import libs
	import sys
	from pyspark import SparkContext
	from pyspark.streaming import StreamingContext

	if __name__ == "__main__":
    	sc = SparkContext(appName="StreamingreduceByKeyAndWindow"); 

    	# 2 is the batch interval : 2 seconds
    ssc = StreamingContext(sc, 2)

    lines = ssc.socketTextStream(à compléter)

    # Counting errors
    ## Split errors
    ## filter using the condition Error in splits 
    ## put one for the concerned errors
    ## Counts the by accumulating the sum
    ## summary function
    ## reverse function
    ## window size = 10
    ## sliding interval = 2
    counts = lines.flatMap(lambda line: line.split(" "))\
        .filter(lambda word:"ERROR" in word)\
        .map(lambda word : (word, 1))\
        .reduceByKeyAndWindow(lambda x, y: int(x) + int(y), lambda x, y: int(x) - int(y), 10, 2)

    ## Affichage
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()

Pourriez-vous expliquez :

-	reduceByKeysAndWindow(.)
-	Quel est l’intérêt de reduceByKeysAndWindow(.) par rapport reduceByWindow(.)

	$ spark-submit ???.py localhost 9999
    




