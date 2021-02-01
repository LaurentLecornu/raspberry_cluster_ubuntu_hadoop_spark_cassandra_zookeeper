# Partie 2/3 : Hadoop 3.2.2 et Spark 3.0.1 sur Ubuntu 20.04 dans un cluster à 4 nœuds

Modifié le : 1/02/2021

Ce texte est inspiré en grande partie par celui de Pier Tarandi [[1]](https://towardsdatascience.com/assembling-a-personal-data-science-big-data-laboratory-in-a-raspberry-pi-4-or-vms-cluster-e4c5a0473025)


On présentera ici l'assemblage et le réglage d'un cluster Raspberry Pi 4 avec Hadoop, Spark, Zookeeper, Kafka

Ce document utilise des commandes en ligne sous linux tel que ssh et nano.

Cette installation a été réalisé à partir d'un mac en utilisant une connexion ssh vers les différents raspberry pi.

Il est conseillé de posséder un cluster d'au moins de trois raspberry car vous devez définir une communication entre divers éléments.


En raison de la taille et pour des raisons pédagogiques, j'ai divisé pour l'instant ce tutoriel en trois parties.

* Partie 1 : Introduction, système opérationnel et mise en réseau (mise en place et réglage du cluster)
* Partie 2 : Hadoop et Spark
* Partie 3 : Zookeeper et Kafka

Tous les fichiers de configuration utilisés seront disponibles à l'adresse [2].

*Avertissement : Ce tutoriel est offert gratuitement à chacun pour une utilisation à vos propres risques. J'ai pris soin de citer toutes mes sources. Étant donné que différentes versions de logiciels peuvent se comporter de manière distincte en raison de leurs dépendances, je vous suggère d'utiliser les mêmes versions que celles que j'ai utilisées.*

## 3. Installation de Hadoop et Spark
L'installation Hadoop et Spark a suivi les instructions de [3, 4].

J'ai utilisé les versions suivantes du site Web d'Apache :

    hadoop-3.2.2.tar.gz
    spark-3.0.1-bin-hadoop3.0.tgz
    
Il vous faudra aller vérifier sur le site de spark et hadoop les numéros des dernières versions disponibles et utiliser les dernières versions.

Attention : seules les versions indiquées dans ce document ont été installées et testées.

### 3.1 Définir votre environnement

Tout d'abord : téléchargez et extrayez les fichiers dans */opt*. Donner accès à l'utilisateur *pi*.

Pour des raisons de simplicité, renommez vos répertoires :

- hadoop-3.2.2 devient hadoop
- spark-3.0.1-bin-hadoop3.2 devient spark

        pi@pi-node13:~$ wget https://downloads.apache.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz
        pi@pi-node13:~$ wget https://mirror.ibcp.fr/pub/apache/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz
        pi@pi-node13:~$ sudo tar -xvf hadoop-3.2.2.tar.gz -C /opt/
        pi@pi-node13:~$ sudo tar -xvf spark-3.0.1-bin-hadoop3.2.tgz  -C /opt/

        pi@pi-node13:~$ cd /opt/
        pi@pi-node13:~$ sudo mv hadoop-3.2.2 hadoop
        pi@pi-node13:~$ sudo mv spark-3.0.1-bin-hadoop3.2 spark
        pi@pi-node13:~$ sudo chown -R pi:pi /opt/spark
        pi@pi-node13:~$ sudo chown -R pi:pi /opt/hadoop
   
ajouter à `/home/pi/.bashrc` :

    ##  path for hadoop and spark

    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
    export HADOOP_HOME=/opt/hadoop
    export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

    export SPARK_HOME=/opt/spark
    export PATH=$PATH:$SPARK_HOME/bin

    export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
    export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH

    export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"

Après édition :

`source /home/pi/.bashrc`

### 3.2 Configuration de Hadoop et de spark sur un seul nœud

Maintenant, vous devez configurer Hadoop et Spark.

Dans un premier temps, on configurera un seul nœud puis on passera à un cluster.

#### 3.2.1 Hadoop

Aller au dossier

`/opt/hadoop/etc/hadoop`


* Modifier le fichier `/opt/hadoop/etc/hadoop/hadoop-env.sh`,

en ajoutant la ligne suivante à la fin :

    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64

* Modifier la configuration dans `/opt/hadoop/etc/hadoop/core-site.xml`

        <configuration>
           <property>
             <name>fs.defaultFS</name>
             <value>hdfs://pi-nodeXX:9000</value>
           </property>
        </configuration>


remplacer `pi-nodeXX` par votre nœud. 
* Modifier la configuration dans `/opt/hadoop/etc/hadoop/hdfs-site.xml`

        <configuration>
          <property>
            <name>dfs.datanode.data.dir</name>
            <value>file:///opt/hadoop_tmp/hdfs/datanode</value>
          </property>
          <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:///opt/hadoop_tmp/hdfs/namenode</value>
          </property>
          <property>
            <name>dfs.replication</name>
            <value>1</value>
          </property>
        </configuration> 


* Préparez maintenant les répertoires suivants :

        pi@pi-node13:~$ sudo mkdir -p /opt/hadoop_tmp/hdfs/datanode
        pi@pi-node13:~$ sudo mkdir -p /opt/hadoop_tmp/hdfs/namenode
    
        pi@pi-node13:~$ sudo chown -R pi:pi /opt/hadoop_tmp

Si les répertoires sont déjà créés. Je conseille un grand nettoyage et la re-création des répertoires.

        $ rm –rf /opt/hadoop_tmp/hdfs/*
        
        pi@pi-node13:~$ sudo mkdir -p /opt/hadoop_tmp/hdfs/datanode
        pi@pi-node13:~$ sudo mkdir -p /opt/hadoop_tmp/hdfs/namenode
    
        pi@pi-node13:~$ sudo chown -R pi:pi /opt/hadoop_tmp



* Modifier la configuration dans `/opt/hadoop/etc/hadoop/mapred-site.xml`

        <configuration>
          <property>
            <name>mapreduce.framework.name</name>
            <value>yarn</value>
          </property>
        </configuration>

* Modifier la configuration dans
`/opt/hadoop/etc/hadoop/yarn-site.xml`

        <configuration>
          <property>
            <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
          </property>
          <property>
            <name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>  
            <value>org.apache.hadoop.mapred.ShuffleHandler</value>
          </property>
        </configuration> 
        
* Modifier la configuration dans
`/opt/hadoop/etc/hadoop/workers`

remplacer `localhost` par `pi-nodeXX`

Il n'y pas de fichier `master`.

* Préparer l'espace de données :

        pi@pi-node13:~$  hdfs namenode -format -force
        pi@pi-node13:~$  start-dfs.sh
        pi@pi-node13:~$  start-yarn.sh
        pi@pi-node13:~$  hadoop fs -mkdir /tmp
        pi@pi-node13:~$  hadoop fs -ls /
        Found 1 items
        drwzr-xr-x - pi supergroup 0 2019-04-09 16:51 /tmp
        
Utilisez *jps* pour vérifier si tous les services sont activés (les chiffres changent..) :

    $ jps
    2736 NameNode
    2850 DataNode
    3430 NodeManager
    3318 ResourceManager
    3020 SecondaryNameNode
    
Vous avez besoin de ces cinq services !

#### 3.2.2 Essais
Pour tester le nœud unique, je me réfère au tutoriel [2] :

Exécutez les commandes suivantes :

On commence par copier un fichier 

    pi@pi-node13:~$ hadoop fs -put $SPARK_HOME/README.md /
    2021-01-23 20:45:30,726 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable

Puis on lance spark-shell

    pi@pi-node13:~$ spark-shell
    2021-01-24 11:35:04,929 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    Spark context Web UI available at http://pi-nodeXX:4040
    Spark context available as 'sc' (master = local[*], app id = local-1611484532293).
    Spark session available as 'spark'.
    Welcome to
       ____              __
      / __/__  ___ _____/ /__
     _\ \/ _ \/ _ `/ __/  '_/
    /___/ .__/\_,_/_/ /_/\_\   version 3.0.1
       /_/
         
    Using Scala version 2.12.10 (OpenJDK 64-Bit Server VM, Java 1.8.0_275)
    Type in expressions to have them evaluated.
    Type :help for more information.

    scala> val textFile = sc.textFile("hdfs://pi-nodeXX:9000/README.md")
    textFile: org.apache.spark.rdd.RDD[String] = hdfs://pi-node13:9000/README.md MapPartitionsRDD[3] at textFile at <console>:24

    scala> textFile.first()
    res1: String = # Apache Spark                                                   

    scala> 

N'oubliez pas de remplacer `pi-nodeXX` par votre nœud

j'ai modifié le fichier suivant `/opt/hadoop/etc/hadoop/capacity-scheduler.xml`.

Le paramètre ***yarn.scheduler.capacity.maximum-am-resource-percent*** doit être défini si vous exécutez un cluster sur une seule machine où vous avez moins de ressources. Ce paramètre indique la fraction des ressources qui sont mises à disposition pour être allouées aux maîtres d'application, ce qui augmente le nombre d'applications simultanées possibles. Notez que cela dépend de vos ressources. Cela a fonctionné dans mon Pi 4 4 Go de bélier.
Modifiez le fichier, en ajoutant la propriété :
/opt/hadoop/etc/hadoop/capacity-scheduler.xml


    <property>
       <name>yarn.scheduler.capacity.maximum-am-resource-percent</name>
       <value>0.5</value>
       <description>
         Maximum percent of resources in the cluster which can be used to 
         run application masters i.e. controls number of concurrent running
         applications.
       </description>
    </property>


###3.3 Hadoop dans un cluster avec Yarn

Maintenant, Il est temps qde créer un cluster Haddop.

*  Création des dossiers pour tous les nœuds :

        $ clustercmd-sudo mkdir -p /opt/hadoop_tmp/hdfs
        $ clustercmd-sudo chown -R pi:pi /opt/hadoop_tmp
        $ clustercmd-sudo mkdir -p /opt/hadoop
        $ clustercmd-sudo chown -R pi:pi /opt/hadoop

Le prochain supprimera toutes les données de Hadoop. Faites d'abord votre sauvegarde s'il y a quelque chose d'important.

        $ clustercmd rm –rf /opt/hadoop_tmp/hdfs/datanode/*
        $ clustercmd rm –rf /opt/hadoop_tmp/hdfs/namenode/*
        
Notez que Spark n'existera que dans le maître.

Copier Hadoop :

À partir de pi-node13 :

     pi@pi1:~$ rsync -vaz /opt/hadoop pi-node14:/opt/hadoop
     pi@pi1:~$ rsync -vaz /opt/hadoop pi-node15:/opt/hadoop
     pi@pi1:~$ rsync -vaz /opt/hadoop pi-node16:/opt/ hadoop

Faites-le pour tous vos nœuds.


Maintenant, les fichiers suivants doivent être modifiés, en modifiant la configuration :
/opt/hadoop/etc/hadoop/core-site.xml

    <configuration>
	   <property>
		  <name>fs.default.name</name>
		  <value>hdfs://pi1:9000</value>
	   </property>
    </configuration>

`/opt/hadoop/etc/hadoop/hdfs-site.xml`

    <configuration>

	  <property>
		  <name>dfs.datanode.data.dir</name>
	     <value>/opt/hadoop_tmp/hdfs/datanode</value>
	  </property>
	
	  <property>
		 <name>dfs.namenode.name.dir</name>
		 <value>/opt/hadoop_tmp/hdfs/namenode</value>
	  </property>
	
	  <property>
		 <name>dfs.replication</name>
		 <value>1</value>
	  </property>

	  <property>
		 <name>dfs.permissions.enabled</name>
		 <value>false</value>
	  </property>
	
    </configuration>

Note — La propriété ***dfs.replication*** indique le nombre de fois que les données sont répliquées dans le cluster. Vous pouvez configurer pour que toutes les données soient dupliquées sur 2 noeuds ou plus.

Note — La dernière propriété, ***dfs.permissions.enabled***, a été définie sur false pour désactiver la vérification des autorisations. 

J'ai également désactivé le mode sans échec. Pour ce faire, après avoir terminé l'exécution de l'installation :
h`dfs dfsadmin -safemode leave`

Si vous le configurez mal, vos applications spark seront bloquées dans le statut "accepté", en raison du manque de ressources.

`/opt/hadoop/etc/hadoop/mapred-site.xml`

    <configuration>

	<property>
		<name>mapreduce.framework.name</name>
		<value>yarn</value>
	</property>

	<property>
		<name>yarn.app.mapreduce.am.env</name>
		<value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
	</property>

	<property>
		<name>mapreduce.map.env</name>
		<value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
	</property>

	<property>
		<name>mapreduce.reduce.env</name>
		<value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
	</property>

	<property>
		<name>yarn.app.mapreduce.am.resource.mb</name>
		<value>512</value>
	</property>

	<property>
		<name>mapreduce.map.memory.mb</name>
		<value>256</value>
	</property>

	<property>
		<name>mapreduce.reduce.memory.mb</name>
		<value>256</value>
	</property>

    </configuration>

`/opt/hadoop/etc/hadoop/yarn-site.xml`

    <configuration>

	<property>
		<name>yarn.acl.enable</name>
		<value>0</value>
	</property>

	<property>
		<name>yarn.resourcemanager.hostname</name>
		<value>pi1</value>
	</property>

	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
	
	<property>
		<name>yarn.nodemanager.resource.memory-mb</name>
		<value>1536</value>
	</property>

	<property>
		<name>yarn.scheduler.maximum-allocation-mb</name>
		<value>1536</value>
	</property>

	<property>
		<name>yarn.scheduler.minimum-allocation-mb</name>
		<value>128</value>
	</property>

	<property>
		<name>yarn.nodemanager.vmem-check-enabled</name>
		<value>false</value>
	</property>

    </configuration>

* créer deux fichiers :

`/opt/hadoop/etc/hadoop/master`

    pi-node13

`/opt/hadoop/etc/hadoop/workers`

    pi-node14
    pi-node15
    pi-node16

Après avoir mis à jour les fichiers de configuration à tous les nœuds, il est nécessaire de formater l'espace de données et de démarrer le cluster (vous pouvez commencer à partir de n'importe quel nœud) :

    $ hdfs namenode -format -force
    $ start-dfs.sh
    $ start-yarn.sh

### 3.4 Configuration de SPARK
Fondamentalement, vous devez créer/modifier le fichier de configuration suivant :
`/opt/spark/conf/spark-defaults.conf`

    spark.master            yarn
    spark.driver.memory     2g
    spark.yarn.am.memory    512m
    spark.executor.memory   512m
    spark.executor.cores    2

Ces valeurs peuvent être ajustées à votre matériel, mais elles fonctionneront avec Raspberry Pi 4 4 Go.
Définissez les variables d'environnement à :
`/opt/spark/conf/spark-env.sh`

    export HADOOP_HOME=/opt/hadoop
    export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop

Installez les paquets suivants dans tous les nœuds afin de permettre aux nœuds de traiter les tâches préparées dans python/pyspark :

    sudo apt install python3 python-is-python3

### 3.5 Test de la grappe
Redémarrez tous les nœuds et redémarrez les services :

    $ start-dfs.sh
    $ start-yarn.sh
Vous pouvez envoyer un exemple d'application pour tester l'étincelle :

    $ spark-submit --deploy-mode client --class org.apache.spark.examples.SparkPi /opt/spark/examples/jars/spark-examples_2.12-3.0.0.jar
À la fin du traitement, vous devriez recevoir un calcul approximatif de la valeur PI :

    Pi is roughly 3.135715678578393
(ce calcul de PI doit être amélioré, c'est le problème avec une méthode monte-carlo)

N'oubliez pas d'arrêter votre cluster 

    $ stop-yarn.sh
    $ stop-dfs.sh 
    
### 3.6 Application Web pour Hadoop et Yarn
#### 3.6.1 Hadoop webUi
http://pi-node13:9870/


http://pi-node13:8088/


[1] P. G. Taranti. https://github.com/ptaranti/RaspberryPiCluster

[2] A. W. Watson. Construire un cluster Raspberry Pi Hadoop / Spark (2019)

[3] W. H. Liang. Construire Raspberry Pi Hadoop/Spark Cluster à partir de zéro (2019)

[4] F. Houbart. Comment installer et configurer un cluster Hadoop à 3 nœuds (2019)