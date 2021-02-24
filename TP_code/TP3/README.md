# **TP 3 : Exécution de Kafka – Exercices sur Kafka**


# 1	Objectif 
* Déploiement de Kafka et Zookeeper
* Test de Kafka en mode cluster et écoute des ports
* Test de Kafka sur un exemple (lecture d’un flux json)
* Intégration de Kafka à Spark streaming


# 2	Déploiement de Kafka – Zookeeper
Afin d’utiliser Kafka, 4 terminaux seront nécessaires :

* Le 1er pour le serveur Zookeeper
* Le 2ème pour le serveur Kafka
* Le 3ème pour le producer
* Le 4ème pour le consumer


## 2.1	Installation et test
Cet énoncé est inspiré par [1].

### 2.1.1	Installation de Zookeeper et de Kafka
La première étape consiste à vérifier la bonne installation et configuration de Kafka et Zookeeper.

Vérifier le contenu du fichier .bashrc afin d’y insérer 
`ZOOKEEPER_HOME` et `KAFKA_HOME` et de modifier `PATH` en y ajoutant les répertoires bin de Kafka et de Zookeeper.

    export KAFKA_HOME=/opt/kafka
    export ZOOKEEPER_HOME=/opt/zookeeper

    export PATH=$PATH:$KAFKA_HOME/bin
    export PATH=$PATH:$ZOOKEEPER_HOME/bin

Voici les étapes utilisées pour installer Kafka et Zookeeper.

    $ #Kafka 2.7.0 installation
    $ wget https://mirror.ibcp.fr/pub/apache/kafka/2.7.0/kafka_2.12-2.7.0.tgz
    $ tar -xzf kafka_2.12-2.7.0.tgz
    $ sudo mv kafka_2.12-2.7.0 /opt/kafka
    $ sudo chown -R pi:pi /opt/kafka
    $ wget https://miroir.univ-lorraine.fr/apache/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz
    $ tar -xzf apache-zookeeper-3.6.2-bin.tar.gz 
    $ sudo mv apache-zookeeper-3.6.2-bin /opt/zookeeper
    $ sudo chown -R pi:pi /opt/zookeeper

(Rappel : ici pi:pi correspond au nom de login et au nom du groupe de celui-ci)

Question : la version de Kafka que vous venez de télécharger contient-elle Zookeeper ?

Tout au long de ce TP, n'hésitez pas à vous référer à la documentation officielle de Kafka.

[https://kafka.apache.org]()

Les binaires de Kafka sont exécutés dans une JVM (Java Virtual Machine) ; vous avez donc besoin d'une installation fonctionnelle de Java dans votre environnement pour poursuivre.

La même que pour Hadoop et Spark.

Pour exécuter Kafka, nous avons besoin de lancer deux composants :

1. Zookeeper, qui est le gestionnaire de cluster de Kafka.
2. Un serveur Kafka que l'on nommera broker.


### 2.1.2	Démarrage du serveur Zookeeper
La version de Kafka que vous avez téléchargée inclut les binaires de Zookeeper ainsi qu'un fichier de configuration prêt à l'emploi. C’est plus simple (mais Kafka n’utilisera qu’un seul nœud).

Zookeeper est le gestion du cluster Kafka.

Pour lancer Zookeeper il suffit donc d'exécuter :

    $ zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties

Ici, on voit l’importance de bien modifier PATH dans .bashrc, sinon 

    zookeeper-server-start.sh
devient

	/opt/kafka/bin/zookeeper-server-start.sh

Remarque : Il est possible de devoir en amont faire un :

   $ ssh pi@pi-nodeXX

Et de passer en ssh (en local pour faire tourner Kafka). Il peut en être de même lors du lancement des services Kafka du producer et du consumer.

Voici le contenu du fichier de configuration de Zookeeper 

    /opt/kafka/config/zookeeper.properties

    dataDir=/tmp/zookeeper
    clientPort=2181
    maxClientCnxns=0

Comme indiqué dans ce fichier de configuration, Zookeeper est un serveur avec lequel on peut communiquer via le port 2181.
 
Comment peut-on vérifier que Zookeeper a été correctement lancé ?


### 2.1.3	Démarrage du serveur Kafka
Maintenant que Zookeeper est lancé, on peut lancer un serveur Kafka :

    $ kafka-server-start.sh /opt/kafka/config/server.properties

Attention : suivant votre quantité de RAM disponible (Raspberry pi 3 ou Raspberry pi 4), vous allez peut-être devoir modifier le fichier kafka-server-start.sh comme suit :

    export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M" # Otherwise, JVM would complain not able to allocate the specified memory.

•	Indiquer ce contient le fichier de configuration 	
`/opt/kafka/config/server.properties` de Kafka

D'après ce fichier de configuration, Kafka écoute désormais sur le port 9092, comment le vérifier ?

(localhost peut être (sera) remplacé par votre nœud)


### 2.1.4	Création d’un topic
Avec une instance de Zookeeper et un broker Kafka qui tournent localement sur votre machine, on dispose d’un « cluster » Kafka minimal qui va permettre de transmettre des messages par le biais d’un (ou des) consumer(s) et d’un (ou des) producer(s). 

Pour envoyer un message, il faut avant tout commencer par créer un topic. 

On crée un topic « conversation » en exécutant le script kafka-topics.sh :

    $ kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic conversation

Notez que je passe à la commande des options qui indiquent le nombre de partitions et le taux de réplication du topic.

Il est possible de vérifier que le topic « conversation » a bien été créé en listant les topics existants par la commande suivante :

    $ kafka-topics.sh --list --zookeeper localhost:2181

Quel est le message obtenu ?

On peut également obtenir quelques propriétés du topic avec l'option --describe passée au même script :

    $ kafka-topics.sh --describe --zookeeper localhost:2181 --topic conversation

-	Quel est le message obtenu ?

-	Pourriez-vous indiquer la définition de :
	* Topic:conversation
	* PartitionCount
	* ReplicationFactor
	* Configs
	* Topic Partition
	* Leader
	* Replicas


### 2.1.5	Démarrage d’un producer
Dans Kafka, les messages sont produits par des producers et consommés par des consumers.

Dans premier temps, nous allons produire quelques messages à la main.

Kafka propose un outil en ligne de commande permettant de produire des messages assez simplement.

Voici la commande pour produire des messages dans le topic « conversation » :

    # Chaque ligne que vous écrirez après cette commande sera considérée comme un message
    $ kafka-console-producer.sh --broker-list localhost:9092 --topic conversation


### 2.1.6	Démarrage d’un consumer
Kafka propose un outil en ligne de commande permettant de consommer des messages assez simplement.

Et voici comment consommer les messages du topic « conversation ». Sur un autre terminal, vous utiliserez la commande suivante :

    $ kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic conversation

Après avoir lancé le producer et le consumer, essayez de taper quelques messages dans l’entrée standard du producer. Ces messages devraient apparaître dans la sortie du consumer.

* Observez-vous une petite latence entre le moment où vous envoyez le message et le moment où il est reçu par le consumer ? Pourquoi ?
* Comment modifier le comportement du producer ?

En l’état, le consumer ne reçoit que les messages envoyés par le producer alors que le consumer est allumé. Il est possible de récupérer tous les messages envoyés dans le topic en passant l’option 
`--from-beginning`. Ceci illustre le fait que les messages sont conservés dans le topic même après avoir été consommés. 

En fait, ils restent dans le topic pendant 168 heures (7 jours) avant d'être effacés ; cette durée est définie par le paramètre log.retention.hours présent dans le fichier de configuration de Kafka.

On aimerait que le consumer traite une seule fois chacun des messages du topic « conversation » : y compris les messages émis alors que le consumer était éteint. Pour cela, il faut assigner le consumer à un groupe. 

Un des rôles de Kafka sera de contrôler où en est chaque groupe de consumers dans la lecture de chaque topic. Pour assigner le consumer à un groupe, il suffit de définir la propriété group.id au moment où l'on lance le consumer :

    $ ./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic conversation --consumer-property group.id=mygroup

Après avoir lancé ce consumer, vous pouvez vérifier que chaque message est transmis une et une seule fois au consumer, et ce même lorsque le consumer est éteint. La liste des groupes de consumers peut être obtenue à l'aide du script kafka-consumer-groups.sh :

    $ ./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

•	Quel est le message reçu ?

Des informations plus précises peuvent être obtenues sur le groupe « mygroup » :

    $ ./bin/kafka-consumer-groups.sh –bootstrap-server localhost:9092 --describe --group mygroup

•	Quel est le message reçu ? Expliquer 

Pour pouvoir passer à l'échelle et faire du Big Data, il va nous falloir plus qu'un seul consumer par topic. On a envie de réaliser des calculs de manière distribuée, donc on aimerait avoir plusieurs consumers différents, sur plusieurs machines, pour un même topic. C'est exactement pour cette raison qu'ont été conçus les groupes dans Kafka. 

Pour l’instant, si on essaie de lancer un second consumer du topic « conversation » dans le groupe « mygroup », avec la même commande que précédemment, on va s'apercevoir qu'un seul des deux consumers va recevoir des messages.

Une partition est une manière de distribuer les données d'un même topic. Lors de la création d'un topic, on indique le nombre de partitions souhaité, comme on l'a vu plus haut avec l'option 
`--partitions` passée à la commande kafka-topics.sh `--create`.

Un topic peut être composé de plusieurs partitions. Chacune de ces partitions contient des messages différents. Lorsqu'un producer émet un message, c'est à lui de décider à quelle partition il l'ajoute. Ce choix d'une partition peut se faire de différentes manières, dont voici quelques exemples (non exhaustifs) :

* Aléatoirement : pour chaque message, une partition est choisie au hasard. C'est ce qui est fait par notre kafka-console-producer.
* Round robin : le producer itére sur les partitions les unes après les autres pour distribuer un nombre de message égal sur chaque partition.
* Hashage : le producer peut choisir une partition en fonction du contenu du message. C'est une fonctionnalité que nous verrons dans le chapitre suivant.

Pour augmenter le nombre de consumers, il faut aussi augmenter le nombre de partitions de notre topic. Quand on a créé le topic « conversation », on n'a créé qu'une seule partition en passant l'option 
`--partitions 1`. Pour modifier le nombre de partitions il faut exécuter la même commande kafka-topics.sh avec l'option –alter :

    $ ./bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic conversation --partitions 2

Avec cette commande on fait passer le nombre de partition à 2. Les nouveaux messages envoyés par le producer seront alors envoyés aléatoirement à l'une ou l'autre des deux partitions ; une partition différente sera affectée à chacun des deux consumers, de manière automatique, et les deux consumers vont donc recevoir des messages différents.

Question : Que doit-on modifier pour passer à un cluster Kafka sur plusieurs nœuds.

 
# 3	Exercice 1 : suivi de l’état des stations de vélos
Nous allons nous intéresser aux solutions de locations de vélo à la demande.

En effet, il existe une API qui permet de contrôler l'état des stations de vélos dans un grand nombre de villes, en France, en Europe et dans le monde grâce à : [https://developer.jcdecaux.com](). Nous allons profiter de cette API pour observer en temps réel les locations à chaque station.


## 3.1	Mode standalone : Kafka sur un seul nœud
Attention : il est conseillé de remplacer localhost par le nom de votre nœud courant et de refaire un ssh : ssh pi@pi-nodecourant avant de lancer les services de kafka, le producer et le consumer.


### 3.1.1	Préparation de la connexion
Pour commencer, vous allez devoir récupérer une clé d'API en créant un compte sur https://developer.jcdecaux.com/#/signup. Une fois que vous aurez créé votre compte, vous disposerez d'une clé d'API affichée dans votre compte utilisateur. Si votre clé d'API est "XXX", vous pouvez vérifier qu'elle fonctionne correctement en récupérant la liste de toutes les stations à l'aide de la commande suivante :

    $ curl https://api.jcdecaux.com/vls/v1/stations?apiKey=XXX

Vous devriez alors obtenir en réponse un gros morceau de JSON assez indigeste. Pour le rendre plus lisible, vous pouvez rediriger la sortie de la commande précédente vers un "prettifier" de JSON (python à un paquet json) :

    $ curl https://api.jcdecaux.com/vls/v1/stations?apiKey=XXX | python -m json.tool

•	Quel est le message affiché ?

Comme on peut le voir, l'API nous fournit le nombre d’emplacements libres ("available_bike_stands") dans chaque station. Si ce nombre augmente (respectivement : diminue) entre deux appels à l'API, c'est que des vélos ont été loués (resp. : déposés) dans la station. Nous allons mettre en place une application qui va afficher l'évolution de ce nombre d'emplacements disponibles, sous la forme suivante :

    +1 MAZARGUES - ROND POINT DE MAZARGUES (OBELISQUE) (Marseille)
    +14 Lower River Tce / Ellis St (Brisbane)
    +2 2 RUE GATIEN ARNOULT (Toulouse)
    +20 ANGLE ALEE ANDRE MURE ET QUAI ANTOINE RIBOUD (Lyon)
    +14 Smithfield North (Dublin)
    +28 52 RUE D'ENGHIEN / ANGLE RUE DU FAUBOURG POISSONIERE - 75010 PARIS (Paris)
    +6 RUE DES LILAS ANGLE BOULEVARD DU PORT - 95000 CERGY (Cergy-Pontoise)
    +6 San Juan Bosco - Santiago Rusiñol (Valence)
    +21 AVENIDA REINA MERCEDES - Aprox. Facultad de Informática (Seville)
    +6 Savska cesta 1 (Ljubljana)
    +31 DE BROUCKERE - PLACE DE BROUCKERE/DE BROUCKEREPLEIN (Bruxelles-Capitale)
    +7 BRICHERHAFF - AVENUE JF KENNEDY / RUE ALPHONSE WEICKER (Luxembourg)
    ...

Pour obtenir le résultat ci-dessus, on pourrait évidemment créer une simple application qui récolterait les données en provenance de l'API et afficherait les différences entre deux appels. Mais une telle application nécessiterait une quantité de mémoire proportionnelle au nombre de stations. Par ailleurs, le traitement des données provoquerait des délais dans les appels à l'API. Enfin, si une des étapes du traitement de données venait à échouer, la collecte des informations serait interrompue.


### 3.1.2	Définition du Producer
Nous allons stocker les données relatives à chaque station de vélos dans des messages Kafka : chacun des éléments de la liste renvoyés par l'appel à l'API ci-dessus va être stocké dans Kafka sous la forme d'une chaîne de caractères au format JSON. Pour cela, nous créons le script velib-get-stations.py qui contient un producer Kafka.

Créer le fichier : `velib-get-stations.py`

    import json
    import time
    import urllib.request

    from kafka import KafkaProducer

    API_KEY = "XXX" # FIXME Set your own API key here
    url = "https://api.jcdecaux.com/vls/v1/stations?apiKey={}".format(API_KEY)

    producer = KafkaProducer(bootstrap_servers="localhost:9092")

    while True:
        response = urllib.request.urlopen(url)
        stations = json.loads(response.read().decode())
        for station in stations:
            producer.send("velib-stations", json.dumps(station).encode())
        print("{} Produced {} station records".format(time.time(), len(stations)))
        time.sleep(1)

N’oubliez pas changer XXX par votre clef.

On peut rencontrer les mêmes problèmes que lors du test (ssh à faire)

On peut remplacer localhost par votre nœud courant.

* Expliquer le script précédent.
* Doit-on l’intégralité du message json lu ? Peut-on le traiter ? A quoi doit-on faire attention ?

Attention : pour exécuter ce script vous aurez besoin du package kafka-python que vous pouvez installer en exécutant (a priori déjà installé)

    $ sudo pip install kafka-python

Nous aurons également besoin d'un cluster Kafka minimal (c’est-à-dire un seul nœud), ainsi que d'un topic « velib-stations ». 

•	Reprenez les explications précédentes pour démarrer un topic « velib-station »

Nous lançons un cluster et créons un topic à l'aide des commandes suivantes (comme expliqué dans le chapitre précédent).
(Ok il nous faut toujours plusieurs terminaux)

Une fois les serveurs démarrés, nous pouvons lancer notre producer qui va envoyer des messages à Kafka en continu :
      
    $ python ./velib-get-stations.py

Notre topic Kafka se remplit progressivement et il nous reste à créer un consumer qui va lire les données de notre topic.

### 3.1.3	Définition du consumer
Nous allons également utiliser le package kafka-python pour développer un consumer. Le rôle de ce consumer est de stocker l'état des différentes stations et d'afficher un message lorsqu'une station change d'état.

Créer le fichier : `velib-monitor-stations.py`

    import json
    from kafka import KafkaConsumer

    stations = {}
    consumer = KafkaConsumer("velib-stations", bootstrap_servers='localhost:9092', group_id="velib-monitor-stations")
    for message in consumer:
        station = json.loads(message.value.decode())
        station_number = station["number"]
        contract = station["contract_name"]
        available_bike_stands = station["available_bike_stands"]

        if contract not in stations:
            stations[contract] = {}
        city_stations = stations[contract]
        if station_number not in city_stations:
            city_stations[station_number] = available_bike_stands

        count_diff = available_bike_stands - city_stations[station_number]
        if count_diff != 0:
            city_stations[station_number] = available_bike_stands
            print("{}{} {} ({})".format("+" if count_diff > 0 else "", count_diff, station["address"], contract))

Dans ce script, nous créons un consumer Kafka pour le topic « velib-stations ». 

•	Pouvez-vous expliquer ce script ?
 
Ce consumer fait partie du groupe « velib-monitor-stations » (consumer = KafkaConsumer("velib-stations", ..., group_id="velib-monitor-stations")). Il suffit de le lancer pour visualiser les fluctuations du nombre d'emplacements libres pour chaque station :

    $ python ./velib-monitor-stations.py

Notez qu'on peut facilement ajouter un producer dans le code de notre consumer. 

* A quoi doit-on faire attention dans notre consumer ?
* Modifier le script ? (comme vous voulez mais en appliquant des filtres,…)


### 3.1.4	Augmentation des partitions

Pour l'instant, nous utilisons un cluster kafka à configuration minimale.

Un producer ajoute des message à un topic doté d'une seule partition et les messages sont récupérés par un unique consumer.
Pour pouvoir passer à l'échelle, comme on l'a décrit dans le chapitre précédent, on va vouloir augmenter le nombre de consumers, ce qui signifie mathématiquement qu'il va falloir augmenter le nombre de partitions de notre topic. On passe à 5 partitions à l'aide de la commande suivante :

    $ ./bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic velib-stations --partitions 10

On peut alors lancer une seconde instance de consumer :

    $ python velib-monitor-stations.py

Nous avons fait évoluer notre application pour obtenir le schéma de fonctionnement suivant :
 
Une moitié des partitions est traitée par le premier consumer, et l'autre moitié est traitée par le second consumer. Le problème qu'on rencontre dans cette nouvelle architecture, est que les deux consumers sont également susceptibles de recevoir les messages qui concernent une même station. 


## 3.2	Passage de Kafka en mode cluster

On refait le même exercice que précédemment à la seule exception que le cluster kafka utilise plusieurs nœuds.

Jusqu'à présent, on a vu comment utiliser Kafka sur une seule machine. : ce genre d'infrastructure est suffisante pour réaliser des tests, mais en production on va avoir besoin de plusieurs niveaux de redondances de manière à ne pas avoir un Single Point Of Failure (SPOF). 

On va configurer Kafka en mode cluster.

On va également utiliser un outil d'administration doté d'une interface web pour contrôler notre cluster.


### 3.2.1	Déploiement d'un cluster distribué

En production, il est nécessaire de disposer de plusieurs serveurs Kafka. Par exemple, si l'on doit redémarrer un cluster, il vaut mieux avoir plusieurs machines que l'on redémarre l'une après l'autre de sorte que l'on n'ait pas d'interruption de service. Pour cela, il faut faire grandir notre cluster de manière horizontale. Ce n'est pas très compliqué : si vous savez déjà comment lancer un serveur (comme on l'a vu dans le chapitre précédent), alors vous savez en lancer plusieurs !

Si vous avez suivi les instructions du chapitre précédent, vous disposez déjà d'un serveur Kafka qui communique avec un serveur Zookeeper. Pour lancer un second serveur Kafka en local, il suffit de modifier sa configuration de sorte qu'elle ne rentre pas en conflit avec celle du premier serveur :

    $ cd kafka
    $ cp config/server.properties config/server1.properties

Les paramètres à modifier dans config/server1.properties sont les suivants :

    $ vim config/server1.properties
    broker.id=1
    listeners=PLAINTEXT://:9093
    log.dirs=/tmp/kafka-logs-1

* Le paramètre broker.idsert d'identifiant unique à notre serveur ; il doit prendre une valeur différente pour chaque serveur.
* L'adresse indiquée par listeners doit être différente de celle sur laquelle va écouter le premier serveur puisque nous faisons tourner les deux serveurs sur la même machine. Notez que si vous exécutez plusieurs serveurs Kafka sur des machines différentes, vous n'avez pas besoin de modifier ce paramètre.
* Le répertoire `log.dirs` dans lequel le serveur Kafka stockera ses données doit être différent d'un serveur à un autre. Là non plus, vous n'aurez pas non plus à modifier ce paramètre si vous exécutez les différents serveurs Kafka sur des machines différentes.

Une fois que ce fichier de configuration a été modifié, on est prêts à lancer un second serveur en passant ce nouveau fichier de configuration en argument :

	$ ./bin/kafka-server-start.sh ./config/server1.properties


### 3.2.2	Réplication des données

Le fait d'avoir plusieurs serveurs Kafka va nous permettre de supporter la panne d'un ou plusieurs serveurs. Mais pour cela, il faut que les données soient correctement répliquées sur les différents serveurs. En effet, si une donnée n'est présente que sur un unique serveur, elle va devenir indisponible lorsque ce serveur tombera en panne ou sera redémarré.

La réplication des données est un paramètre que l'on peut ajuster lors de la création d'un topic. Dans les chapitres précédents on a utilisé l'option `--replication-factor 1` lors de la création de nos topics. Pour augmenter le taux de réplication d'un topic, il suffit de modifier ce paramètre :

	$ ./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 10 --topic velib-stations

En exécutant cette commande, on a créé un topic "velib-stations" doté de dix partitions et d'un taux de réplication de 2. Cela signifie que les données seront systématiquement répliquées sur deux serveurs, ce qui devrait nous prémunir contre la panne d'un serveur.

De manière générale, si le taux de réplication est de N, l'architecture permettra de supporter la panne de N-1 serveurs.
Pour pouvoir recréer le topic "velib-stations", vous allez probablement devoir le supprimer avant. La suppression d'un topic n'est possible que si le fichier de configuration du serveur comprend la clause `delete.topic.enable=true`.

On peut vérifier que les partitions sont bien distribuées entre les serveurs avec la commande suivante :

	$ ./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic velib-stations

•	Quel est le message affiché ? (interpréter)

Le résultat de cette commande indique que chaque partition possède un leader attitré : le leader est responsable de l'écriture des données par les producers et de la lecture des données par les consumers. Cependant, il n'est pas du ressort des producers ni des consumers d'adresser leurs requêtes au leader de chacune des partitions. Il suffit d'indiquer au producer ou au consumer l'adresse d'un ou plusieurs brokers du cluster ; les requêtes en écriture et en lecture seront automatiquement transmises au leader de chacune des partitions.

La commande ci-dessus indique également sur quel broker se trouve chacune des replicas de chaque partition ainsi que les in sync replicas (ISR). Les ISR correspondent aux replicas contenant des versions à jour des données.

Pour tester la résilience de notre nouveau cluster, il suffit d'éteindre un des brokers. Éteignons par exemple le broker 0 et exécutons à nouveau la commande précédente :

	$ ./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic velib-stations

•	Quel est le message affiché ? (Analyser l’évolution)

Comme on peut le voir, le seul broker qui fonctionne encore est maintenant le nouveau leader qui a été assigné à chacune des partitions ; celles-ci ne disposent plus qu'une d'une seule ISR. 

En production il s'agirait ici d'un événement "orange" (entre le rouge et le vert) : il n'y a pas eu de perte de données, mais il suffirait qu'un serveur supplémentaire soit arrêté pour rendre tout le service indisponible.

Il est possible de tester notre architecture avec notre couple de producer/consumer. Il faut simplement indiquer l'adresse de plusieurs brokers, de sorte que la production et la réception de message fonctionne même en cas de panne d'un des serveurs :

	producer = KafkaProducer(bootstrap_servers=['localhost:9092', 'localhost:9093'])
	consumer = KafkaConsumer(..., bootstrap_servers=['localhost:9092', 'localhost:9093'], ...)

N'hésitez pas à tester un couple producer/consumer en éteignant et en rallumant alternativement l'un des deux brokers. Vous pourrez également vérifier que lorsque les deux brokers sont à nouveau fonctionnels, ils deviennent à nouveau chacun leader de la moitié des partitions. Cependant, par défaut ce changement n'intervient que toutes les cinq minutes. Pour accélérer le ré-équilibrage des partitions, vous pouvez modifier le paramètre leader.imbalance.check.interval.seconds dans le fichier de configuration des brokers.


 
# 4	Exercice 2 :Exemple d’utilisation de Kafka avec spark
## 4.1	Ingestion des données dans Kafka
Le code suivant permet le lancement des serveurs ZooKeeper et Kafka ainsi que la création des topics :

	/opt/kafka/bin/zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
	/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
	/opt/kafka/bin/kafka-topics.sh \
	--create --zookeeper localhost:2181 --replication-factor 1 \
	--partitions 1 --topic taxirides
	/opt/kafka/bin/kafka-topics.sh \
		--create --zookeeper localhost:2181 --replication-factor 1 \
	--partitions 1 --topic taxifares

Cet exercice est totalement inspiré de l’article de RYNKIEWICZ Oskar [3].

Nous aborderons dans un premier temps l’aspect streaming et nous présenterons un cas d’usage. Les données seront ingérées avec Kafka puis traitées en temps quasi réel dans Spark Structured Streaming. 

Un jeu de données de taxi new-yorkais seront utilisées. Ce dataset contient une collection de courses référencées par conducteur ainsi que des informations telles que la somme payée, la date ou encore une variable indicatrice nous informant si la course commence ou se termine, etc. Ces données sont disponibles dans les deux fichiers compressés de ce site : nycTaxiRides.gz fournit les informations géographiques, nycTaxiFares.gz les informations pécuniaires. Ses deux fichiers ne sont pas gourmands en termes de mémoire (la taille en dessous de 100MB). Autrement, la base de données originale dépasse les 500GB et correspondra, de ce fait, à un environnement type cluster.

La problématique de ce cas d’usage sera d’identifier les zones géographiques de Manhattan (les quartiers) où les chauffeurs seraient le plus à même de recevoir un pourboire élevé. Un conducteur ayant cette information pourrait ainsi choisir stratégiquement son secteur d’activité. A noter que les données concernant les pourboires sont disponibles seulement lorsque le client règle en carte bancaire. L’analyse en sera impactée, mais ne perd pas totalement son sens. Cette problématique s’applique à l’environnement streaming. En effet, l’obtention rapide d’un résultat permettra aux conducteurs de s’orienter vers lesdites zones le plus tôt possible.

Dans une application réelle, garder à l’esprit que les données ne sont pas bornées et qu’il s’agit d’un flux continu. Pour avoir la flexibilité de cet apprentissage, le jeu de données est borné. Néanmoins, nous simulerons un flux de données puisque les données sont émises en tant qu’événements en cours dans Kafka. Pour cela, on va couper le fichier en petits morceaux transmis les uns après les autres. Aucune modification n’est nécessaire entre cette variante et ce qui se passerait réellement. Le code ci-dessous, grâce à des pipes Unix, importe les données dans les topics concernés :

	( curl -s https://training.ververica.com/trainingData/nycTaxiRides.gz \
	| zcat \
	| split -l 10000 --filter="/opt/kafka/bin/kafka-console-producer.sh \
	--broker-list localhost:9092 --topic taxirides; sleep 0.2"\
	> /dev/null ) &
	( curl -s https://training.ververica.com/trainingData/	nycTaxiFares.gz \
	| zcat \
	| split -l 10000 --filter="/opt/kafka/bin/kafka-console-producer.sh \
	--broker-list localhost:9092 --topic taxifares; sleep 0.2" \
	> /dev/null ) &

En détaillant ce code, il en ressort que :

1.	Un stream est créé depuis le fichier compressé, aucun fichier n’est stocké à l’ordinateur
1.	La commande zcat permet de lire le contenu d’un fichier compressé
1.	La commande split permet d’envoyer des données vers –filter en les regroupant en blocs de 10000 messages
1.	Les événements sont publiés vers le topic Kafka avec le script kafka-console-producer.sh
1.	La commande sleep produit un délai de 100 milliseconds entre chaque “batch” de messages, on cherche ici à reproduire la nature séquentiel d’un stream
1.	Sachant que le producer Kafka produit le caractère > pour chaque évènement, on redirige ces caractères vers /dev/null
1.	Le caractère & permet de faire tourner cette commande en tâche de fond. Il libère le terminal pour lancer immédiatement un autre stream

Deux streams de données sont simulés dans cet exemple. Une situation réelle en impliquerait bien plus, émanant de plusieurs centaines de machines (cas d’un réseau IoT, par exemple). Les producers Kafka seraient également complexifiés. 

Les consumers Kafka peuvent être utilisés pour vérifier la bonne ingestion de nos données dans les topics. Utiliser les commandes suivantes afin de voir apparaître vos résultats dans la console :

	/opt/kafka/bin/kafka-console-consumer.sh \
	--bootstrap-server localhost:9092 --topic taxirides --from-beginning
	/opt/kafka/bin/kafka-console-consumer.sh \
	--bootstrap-server localhost:9092 --topic taxifares –from-beginning

Les données transitent désormais dans le bus de message qu’est Kafka, concentrons maintenant notre attention sur l’application Spark.


## 4.2	Intégration de Spark Structured Streaming avec Kafka
Le même code utilisé pour les traitements batch peut s’appliquer à du streaming, seules les méthodes d’entrées et de sorties devraient être modifiées. 

La première étape consiste en la création d’une Session Spark. Nous récupérerons ensuite nos données de streamings depuis les topics Kafka, et les mettrons sous forme de DataFrame. 

    from pyspark.sql import SparkSession
    spark = SparkSession.builder \
        .appName("Spark Structured Streaming from Kafka") \
  	    .getOrCreate()

    sdfRides = spark \
       .readStream \
       .format("kafka") \
       .option("kafka.bootstrap.servers", "localhost:9092") \
       .option("subscribe", "taxirides") \
       .option("startingOffsets", "latest") \
       .load() \
       .selectExpr("CAST(value AS STRING)") 

    sdfFares = spark \
       .readStream \
       .format("kafka") \
       .option("kafka.bootstrap.servers", "localhost:9092") \
       .option("subscribe", "taxifares") \
       .option("startingOffsets", "latest") \
       .load() \
       .selectExpr("CAST(value AS STRING)")

Il faudra remplacer localhost par son nœud.

L’option startingOffsets est réglée sur latest, nous obligeant à relancer le flux de données dans Kafka lorsque l’application Spark attend des données. Nous sélectionnons seulement la colonne « value », contenant nos données de Taxi sous forme de la chaîne de caractères. Les autres colonnes contiennent des métadonnées qui pourraient être utiles dans un environnement de production. Avant d’extraire les données, préparons le schéma afin de leurs donner du sens. Préparons les schémas de nos DataFrames en définissant les noms de nos attributs. Nous pourrons ensuite injecter les données dans les nouvelles colonnes.

    from pyspark.sql.types import *

    taxiFaresSchema = StructType([ \
       StructField("rideId", LongType()), StructField("taxiId",  
       LongType()), \
       StructField("driverId", LongType()), StructField("startTime", TimestampType()), \
      StructField("paymentType", StringType()), StructField("tip", FloatType()), \
      StructField("tolls", FloatType()), StructField("totalFare", FloatType())])
    
    taxiRidesSchema = StructType([ \
        StructField("rideId", LongType()), StructField("isStart", StringType()), \
        StructField("endTime", TimestampType()), StructField("startTime", TimestampType()), \
        StructField("startLon", FloatType()), StructField("startLat", FloatType()), \
        StructField("endLon", FloatType()), StructField("endLat", FloatType()), \
        StructField("passengerCnt", ShortType()), StructField("taxiId", LongType()), \
        StructField("driverId", LongType())])

    def parse_data_from_kafka_message(sdf, schema):
        from pyspark.sql.functions import split
        assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
        col = split(sdf['value'], ',') #split attributes to nested array in one Column
        #now expand col to multiple top-level columns
        for idx, field in enumerate(schema): 
            sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
       return sdf.select([field.name for field in schema])

    sdfRides = parse_data_from_kafka_message(sdfRides, taxiRidesSchema)
    sdfFares = parse_data_from_kafka_message(sdfFares, taxiFaresSchema)

Comment peut-on vérifier que la structure des données proposée est la bonne ?

Et maintenant, on peut traiter les dataframes récupérés.

•	Soyez imaginatif et ajouter un traitement sur votre dataframe.


## 4.3	Requêtes streaming dans Spark
Il est bon de vérifier la disponibilité de nos données en lançant une requête simple retournant le nombre de courses effectuées par conducteur :

    query = sdfRides.groupBy("driverId").count()

    query.writeStream \
       .outputMode("complete") \
       .format("console") \
       .option("truncate", False) \
       .start() \
       .awaitTermination()

L’interface DataFrame.writeStream contrôle le comportement d’envoi de nos données streaming. 

* Trois modes d’output sont à notre disposition, déterminant quels résultats (quelles lignes du “Result Table”) seront envoyés au collecteur de données externe :
	* outputMode("complete") utilisé au-dessus, s’applique dans le cas des requêtes agrégées. Toutes les lignes sont utilisées lors du traitement de la requête
	* outputMode("update") sera utile dans le cas où vous voulez seulement considérer les nouvelles lignes et les lignes modifiés depuis le dernier trigger
	* outputMode("append") où seuls les nouvelles lignes seront prise en compte, précisément une fois. Les résultats précédents sont déjà affichés et, par conséquent, ne sont pas modifiables. En effet, il est impossible de modifier le contenu d’un fichier existant en ajoutant une nouvelle ligne de caractère. Seules les requêtes donnant un résultat unique (i.e select, filter) sont supportées. Les requêtes aggrégés (i.e count) ne fonctionneront pas dans ce mode, à part si vous utilisez le watermarking et le Windowing
* Le format("console") est modifiable selon l’utilisation. Un autre topic Kafka, un fichier sink auraient pu être spécifiés comme un collecteur de données externe 
* Une requête Spark Structured Streaming peut être déclenchée à l’aide de triggers spécifiant l’intervalle de temps entre chaque exécution de micro-batch. L’option .trigger() n’a pas été spécifiée, Spark procédera les nouvelles données une fois que le micro-batch précédent arrivera à terme

Soit 

    spark/bin/spark-submit \
        --master local --driver-memory ?g \
        --num-executors ?g --executor-memory ?g \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4 \
        sstreaming-spark-out.py

•	Fixer les points d’interrogation

Une fois l’application Spark active et renvoyant un résultat vide ‘Batch : 0’ avec les noms des colonnes, il est temps de relancer le stream des données avec la commande Kafka expliqué précédemment :

    ( curl -s https://training.ververica.com/trainingData/nycTaxiRides.gz \
	| zcat \
	| split -l 10000 --filter="kafka/bin/kafka-console-producer.sh \
	--broker-list localhost:9092 --topic taxirides; sleep 0.2" \
	> /dev/null ) &


## 4.4	Nettoyage des données
C’est une tâche parfois fastidieuse mais essentielle au bon déroulement des requêtes. Nous portons notre étude sur la zone de Manhattan, il semble donc logique d’évincer les courses ne commençant pas ou ne finissant pas dans le périmètre de New York. Les évènements “START” sont également mis de côté car nous voulons les courses ayant débouchés sur un paiement, et possiblement un pourboire. Afin d’éviter toute confusion, l’ordre des colonnes “endTime” et “startTime” de sdfRides est inversé respectivement pour “START” et “END”. Aussi, sachant que seuls les évènements “END” sont gardés, un seul ordre est préservé.

	LON_EAST, LON_WEST, LAT_NORTH, LAT_SOUTH = -73.7, -74.05, 41.0, 40.5
	sdfRides = sdfRides.filter( \
        sdfRides["startLon"].between(LON_WEST, LON_EAST) & \
        sdfRides["startLat"].between(LAT_SOUTH, LAT_NORTH) & \
        sdfRides["endLon"].between(LON_WEST, LON_EAST) & \
        sdfRides["endLat"].between(LAT_SOUTH, LAT_NORTH))
    # Notice that rides with faulty geospatial data as e.g. (0, 0) are filtered out also 

    sdfRides = sdfRides.filter(sdfRides["isStart"] == "END") #Keep only finished!

•	Choisir une autre zone, un autre critère


## 4.5	Jointure stream-stream grâce au Watermarking
Spark 2.3 introduit la jointure stream-stream. Le but est de joindre les deux DataFrames sdfRides et sdfFares qui sont en train de recevoir leur stream. En combinant données spatio-temporelles et financières, on augmente le nombre de paramètres à calculer. 

Ce type de jointure n’est réalisable que dans le mode output("append"). Ces jointures peuvent bénéficier du concept de Watermarking, ce concept devrait être considéré comme essentiel pour réaliser des jointures.

Le watermark définit le délai qu’un timestamp peut prendre par rapport au temps maximal de l’événement observé jusqu’à présent. Prenons un exemple, le dernier événement a eu lieu à 14h05 et le watermark est défini sur 1 heure. Un nouvel événement apparaissant à 13h00 serait supprimé tandis que celui de 13h10 serait marqué comme valide et conservé en mémoire. Ce mécanisme limite la taille du buffer pour les jointures et garantit que les données ne se développent pas infiniment. Un événement n’est pas gardé éternellement pour un jointure ou un aggrégat. La suppression des données obsolètes résout également les problèmes de données hors cadre (out-of-order data).

Le but de cette jointure est de rassembler deux évènements concernés par un même sujet, la fin de la course, et non de lier les évènements selon le début et la fin de la course. Une stratégie consisterait à mettre un watermark sur la variable “endTime” des deux DataFrames et de définir une contrainte sur la différence de temps sur la variable de fin de course. Malheureusement, sdfFares n’a pas la variable “endTime”, seulement “startTime”. Une solution serait donc de baser la jointure en fixant deux watermark : sur “startTime” pour sdfFares et sur “endTime” pour sdfRides. Une contrainte de temps relative au début et à la fin de la course doit être envisagé pour la jointure. 

    # Apply watermarks on event-time columns
    sdfFaresWithWatermark = sdfFares \
        .selectExpr("rideId AS rideId_fares", "startTime", "totalFare", "tip") \
        .withWatermark("startTime", "30 minutes")  # maximal delay

    sdfRidesWithWatermark = sdfRides \
        .selectExpr("rideId", "endTime", "driverId", "taxiId", \
        "startLon", "startLat", "endLon", "endLat") \
        .withWatermark("endTime", "30 minutes") # maximal delay

    # Join with event-time constraints
    sdf = sdfFaresWithWatermark \
        .join(sdfRidesWithWatermark, \
    expr(""" 
     rideId_fares = rideId AND 
      endTime > startTime AND
      endTime <= startTime + interval 2 hours
      """))

Nous avons fixé ci-dessus que les évènements des DataFrames ne pouvait pas dépasser 30 minutes. Un évènement sdfFares est gardé 30 minutes afin de matcher son homologue dans sdfRides, et vice versa. La contrainte utilisé pour la jointure écarte également les courses supérieures à 2 heures.

 
# 5	Références
[1] 	[https://openclassrooms.com/fr/courses/4451251-gerez-des-flux-de-donnees-temps-reel/4451521-metamorphosez-vos-applications-temps-reel-avec-kafka]()

[2]	[https://openclassrooms.com/fr/courses/4451251-gerez-des-flux-de-donnees-temps-reel/4451526-creez-votre-premiere-application-avec-kafka]()

[3] 	[https://www.adaltas.com/fr/2019/04/18/spark-streaming-data-pipelines-structured-streaming/ par RYNKIEWICZ Oskar ]()consulté le 14/02/2020






