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

	spark.master            spark://ip-node-master-spark:7077
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

 


