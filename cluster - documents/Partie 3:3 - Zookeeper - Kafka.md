# Partie 4/4 : Kafka et Zookeeper sur Ubuntu dans un cluster à 4 nœuds

Ce texte est inspiré en grande partie par celui de Pier Tarandi [[1]](https://towardsdatascience.com/kafka-and-zookeeper-over-ubuntu-in-a-3-node-cluster-a-data-science-big-data-laboratory-part-4-of-4-47631730d240)



Assemblage d'un cluster Raspberry Pi 4 avec Hadoop, Spark.


Le texte suppose que vous connaissez et savez utiliser les commandes en ligne sous linux, y compris ssh, vim et nano.

Cette installation a été réalisé à partir d'un mac en utilisant une connexion ssh vers les différents raspberry pi.

Il est conseillé de posséder un cluster d'au moins de trois raspberry car vous devez définir une communication entre divers éléments.


En raison de la taille et pour des raisons pédagogiques, j'ai également diviser ce tutoriel en deux parties.

* Partie 1 : Introduction, système opérationnel et mise en réseau (mise en place et réglage du cluster)
* Partie 2 : Hadoop et Spark
* Partie 3 : Zookeeper et Kafka

Tous les fichiers de configuration utilisés seront disponibles à l'adresse [2].

*Avertissement : Ce tutoriel est offert gratuitement à chacun pour une utilisation à vos propres risques. J'ai pris soin de citer toutes mes sources. Étant donné que différentes versions de logiciels peuvent se comporter de manière distincte en raison de leurs dépendances, je vous suggère d'utiliser les mêmes versions que celles que j'ai utilisées lors de votre premier essai.*

##6. Kafka

Kafka (https://kafka.apache.org/) est un broker de messages robuste largement utilisé pour instancier des pipelines. Sa fonctionnalité de rétention permet de gérer une vague d'informations ou la nécessité de mettre les consumers hors ligne pour maintenance.

En outre, comme presque toutes les solutions de big data, Kafka passe rapidement d'un seul nœud à des clusters complets avec réplication.

La littérature principale pour apprendre le kafka est le livre "Kafka : Le guide définitif" [[2]](https://www.confluent.io/resources/kafka-the-definitive-guide/). 

Un grand merci à Confluent !

Kafka peut facilement gérer de gigaoctets à même pétaoctets par jour. C'est loin d'être ma capacité de ce cluster. Cependant, j'ai décidé d'installer Kafka initialement en tant que nœud unique et de l'avoir distribué pour permettre de jouer avec les pipelines de données, comme la collecte d'informations en temps réel à partir de Tweeter.

###6.1 Zookeeper

La première étape consiste à installer le serveur zookeeper puisque Kafka en dépend pour la distribution des métadonnées. J'ai installé la version stable la plus récente disponible sur les sites suivants :
> https://zookeeper.apache.org/releases.html

> https://downloads.apache.org/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2.tar.gz

    pi@pi-node13:~$ wget https://downloads.apache.org/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz
    pi@pi-node13:~$ tar -xzvf apache-zookeeper-3.6.2-bin.tar.gz
    sudo mv apache-zookeeper-3.6.2-bin /opt/zookeeper

    pi@pi-node13:~$ cd /opt
    pi@pi-node13:/opt$ ls
    hadoop  hadoop_tmp  spark  zookeeper
    pi@pi-node13:/opt$ sudo chown -R pi:pi zookeeper
    pi@pi-node13:/opt$ sudo mkdir /opt/zookeeper_data
    pi@pi-node13:/opt$ sudo chown -R pi:pi zookeeper_data


Créez le fichier :
`/opt/zookeeper/conf/zoo.cfg`

    # see zoo_sample.cfg_old for information about parameters

    tickTime=2000
    dataDir=/opt/zookeeper_data
    clientPort=2181
    initLimit=20
    syncLimit=5

    # this parameters are for a zookeeper cluster (assemble)
    #server.1=pi-node13:2888:3888
    #server.2=pi-node14:2888:3888
    #server.3=pi-node15:2888:3888

Maintenant, vous pouvez démarrer zookeeper dans un seul nœud :

sudo netstat -plnt | grep 2181

    pi@pi-node13:/opt/zookeeper/conf$ /opt/zookeeper/bin/zkServer.sh start
    ZooKeeper JMX enabled by default
    Using config: /opt/zookeeper/bin/../conf/zoo.cfg
    Starting zookeeper ... STARTED
    pi@pi-node13:/opt/zookeeper/conf$ sudo netstat -plnt | grep 2181
    tcp6       0      0 :::2181                 :::*                    LISTEN      18641/java  



Maintenant, nous avons zookeeper qui fonctionne localement sur pi-node13. Ensuite, nous pouvons installer Kafka.

### 6.2 KAFKA

L'installation de Kafka sur un seul nœud n'est pas si gênante. 

J'ai téléchargé la version stable la plus récente, qui était
`kafka_2.13–2.7.0.tgz`


	pi@pi-node13:~$ wget https://downloads.apache.org/kafka/2.7.0/kafka_2.13-2.7.0.tgz 

	pi@pi-node13:~$ tar -xzvf kafka_2.13-2.7.0.tgz

    pi@pi-node13:~$ cd /opt
    pi@pi-node13:/opt$ ls
    hadoop  hadoop_tmp  kafka  spark  zookeeper  zookeeper_data
    pi@pi-node13:/opt$ sudo chown -R pi:pi kafka
    pi@pi-node13:/opt$ sudo mkdir /opt/kafka_data
    pi@pi-node13:/opt$ sudo chown -R pi:pi  /opt/kafka_data


* Modifier le fichier
`/opt/kafka/config/server.properties`,

en modifiant le paramètre suivant :
   
    log.dirs=/opt/kafka_data

* Démarrer Kafka :

        pi@pi-node13:/opt$ /opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
        
Remarque : Kafka et Zookeeper ont besoin d'un terminal ouvert si vous n'indiquez pas un autre moyen. Lors du démarrage de ces services. Utilisez d'abord une session terminale/à distance pour chaque service. 

Après le tutoriel, vous montrerez comment le faire de manière transparente.

* Vérification du port 9092 :

        pi@pi-node13:/opt$ sudo netstat -plnt | grep 9092
        tcp6       0      0 :::9092                 :::*                    LISTEN      19148/java        



Les commandes suivantes vous permettront de vous assurer que Kafka fonctionne correctement :

1. Démarrer Zookeeper :

        pi@pi-node13:/opt$ /opt/zookeeper/bin/zkServer.sh start
        ZooKeeper JMX enabled by default
        Using config: /opt/zookeeper/bin/../conf/zoo.cfg
        Starting zookeeper ... already running as process 18641.

2. Démarrer Kafka et créer un sujet Kafka avec le producteur et le consommateur et le tester :
        
        pi@pi-node13:/opt$ /opt/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
        Created topic test.
        
        pi@pi-node13:/opt$ /opt/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 

        pi@pi-node13:/opt$ /opt/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic test
        Topic: test	PartitionCount: 1	ReplicationFactor: 1	Configs: 
	    Topic: test	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
	    
        pi@pi-node13:/opt$ /opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
        >test test
        >message test
                   
        >^Cpi@pi-node13:/opt$ /opt/kafka/bin/kafka-console-consumer.sh  --bootstrap-server localhost:9092 --topic test --from-beginning
        test test
        message test
        ^CProcessed a total of 2 messages


### 6.3 Changement de Zookeeper et de Kafka en mode cluster
Attention : Kafka et Zookeeper suggèrent que vous avez un nombre impair de nœuds. Je les utilise, c'est correct.

* **pi-node14**

        pi@pi-node14:~$ sudo mkdir /opt/zookeeper_data
        pi@pi-node14:~$ sudo mkdir /opt/zookeeper
        pi@pi-node14:~$ sudo mkdir /opt/kafka
        pi@pi-node14:~$ sudo mkdir /opt/kafka_data
    
        pi@pi-node14:~$ sudo chown -R pi:pi /opt/zookeeper_data
        pi@pi-node14:~$ 
        pi@pi-node14:~$ sudo chown -R pi:pi /opt/zookeeper
        pi@pi-node14:~$ sudo chown -R pi:pi /opt/kafka
        pi@pi-node14:~$ sudo chown -R pi:pi /opt/kafka_data


* **pi-node15**

        pi@pi-node15:~$ sudo mkdir /opt/zookeeper_data
        pi@pi-node15:~$ sudo mkdir /opt/zookeeper
        pi@pi-node15:~$ sudo mkdir /opt/kafka
        pi@pi-node15:~$ sudo mkdir /opt/kafka_data
    
        pi@pi-node15:~$ sudo chown -R pi:pi /opt/zookeeper_data
        pi@pi-node15:~$ 
        pi@pi-node15:~$ sudo chown -R pi:pi /opt/zookeeper
        pi@pi-node15:~$ sudo chown -R pi:pi /opt/kafka
        pi@pi-node15:~$ sudo chown -R pi:pi /opt/kafka_data


* **pi-node13**
 
        pi@pi-node13:/opt$ rsync -vaz /opt/zookeeper/ pi-node14:/opt/zookeeper/
        pi@pi-node13:/opt$ rsync -vaz /opt/kafka/ pi-node14:/opt/kafka/
        pi@pi-node13:/opt$ rsync -vaz /opt/zookeeper/ pi-node15:/opt/zookeeper/
        pi@pi-node13:/opt$ rsync -vaz /opt/kafka/ pi-node15:/opt/kafka/
        
* Modifier en supprimant les commentaires précédents (pi-node13, pi-node14, pi-node15)
`/opt/zookeeper/conf/zoo.conf`

créer des fichiers :
/opt/zookeeper_data/myid
Le fichier ne doit avoir que l'id du nœud zookeeper (voir GitHub)

pi1 ->1,

pi2 ->2,

pi3 ->3,

* Pour Kafka, nous devons éditer (dans tous les nœuds) :
`/opt/kafka/config/server.properties`

        ############################# Server Basics #############################

        # The id of the broker. This must be set to a unique integer for each broker.
        ## THIS IS FOR pi3 NODE
        broker.id=3

        ############################# Socket Server Settings #############################

        num.network.threads=3
        num.io.threads=8
        socket.send.buffer.bytes=102400
        socket.receive.buffer.bytes=102400
        socket.request.max.bytes=104857600

        ############################# Log Basics #############################

        # A comma separated list of directories under which to store log files
        log.dirs=/opt/kafka_data
        num.partitions=1
        num.recovery.threads.per.data.dir=1

        ############################# Internal Topic Settings  #############################
        offsets.topic.replication.factor=1
        transaction.state.log.replication.factor=1
        transaction.state.log.min.isr=1

        ############################# Log Retention Policy #############################
        log.retention.hours=168
        log.segment.bytes=1073741824
        log.retention.check.interval.ms=300000

        ############################# Zookeeper #############################
        zookeeper.connect= pi1:2181, pi2:2181, pi3:2181
        zookeeper.connection.timeout.ms=18000

        ############################# Group Coordinator Settings #############################
        group.initial.rebalance.delay.ms=0


* Modification des paramètres :

           broker.id=1 # 2, 3 selon le nœud
(1 pour pi-node&", 2 pour pi-node14 et 3 pour pi-node15

et :

`zookeeper.connect= pi1:2181, pi2:2181, pi3:2181`

Maintenant, Zookeeper et Kafka fonctionneront en cluster. Vous devez le démarrer dans tous les nœuds.


## 7. Démarrage du cluster

J'ai codé un script pour chaque nœud, pour démarrer tous les services - parce que j'oublie parfois de démarrer des services spécifiques. Vous trouverez les scripts dans le dossier d'accueil de l'utilisateur pi sous le nom de cluster-start.sh. 

Le script utilise des connexions ssh pour démarrer des services dans les autres nœuds, et je l'ai copié sur tous mes nœuds.
`/home/pi/cluster-start.sh`

    echo zookeeper pi-node13
    ssh pi-node13 '/opt/zookeeper/bin/zkServer.sh start > /dev/null 2>&1 &'
    echo zookeeper pi-node14
    ssh pi-node14 '/opt/zookeeper/bin/zkServer.sh start > /dev/null 2>&1 &'
    echo zookeeper pi-node15
    ssh pi-node15 '/opt/zookeeper/bin/zkServer.sh start > /dev/null 2>&1 &'

    echo kafka pi-node13
    ssh pi-node13 '/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties > /dev/null 2>&1 &'
    echo kafka pi-node14
    ssh pi-node14 '/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties > /dev/null 2>&1 &'
    echo kafka pi-node15
    ssh pi-node15 '/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties > /dev/null 2>&1 &'


    echo start hadoop cluster
    start-dfs.sh
    echo start yarn
    start-yarn.sh

    echo 'Thunderbirds Go !'

et le script pour tout arrêter `/home/pi/cluster-stop
.sh`

    echo zookeeper pi-node13
    ssh pi-node13 '/opt/kafka/bin/kafka-server-stop.sh > /dev/null 2>&1 &'
    echo zookeeper pi-node14
    ssh pi-node14 '/opt/kafka/bin/kafka-server-stop.sh > /dev/null 2>&1 &'
    echo zookeeper pi-node15
    ssh pi-node15 '/opt/kafka/bin/kafka-server-stop.sh > /dev/null 2>&1 &'

    echo kafka pi-node13
    ssh pi-node13 '/opt/zookeeper/bin/zkServer.sh stop > /dev/null 2>&1 &'
    echo kafka pi-node14
    ssh pi-node14 '/opt/zookeeper/bin/zkServer.sh stop > /dev/null 2>&1 &'
    echo kafka pi-node15
    ssh pi-node15 '/opt/zookeeper/bin/zkServer.sh stop > /dev/null 2>&1 &'


    echo stop yarn
    stop-yarn.sh
    echo stop hadoop cluster
    stop-dfs.sh

    echo 'FIN'



Vous pouvez vérifier l'état du cluster à l'aide de l'interface utilisateur Web pour Hadoop, Yarn et l'outil Kafka.

