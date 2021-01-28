# Partie 1/3 : Cluster Raspberry Pi 

Ce texte est inspiré en grande partie par celui de Pier Tarandi [[1]](https://towardsdatascience.com/assembling-a-personal-data-science-big-data-laboratory-in-a-raspberry-pi-4-or-vms-cluster-ff37759cb2ec)



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

## 1. Introduction

L'objectif est de reproduire dans un cadre pédagogique et à un coût limité des cluster big dat.

Sur  cet environnement, j'utiliserai des solutions prises en charge par Apache  : Hadoop, Spark  installées sur un cluster. 

L'environnement Big Data nécessite une solution distribuée dans le monde réel - l'évolutivité est une exigence primordiale. Ainsi, apprendre à configurer l'environnement est important pour moi dans un cadre pédagogique. C'est pourquoi je n'utiliserais pas pour cela  des solutions basées sur le cloud.

Le nouveau Raspberry Pi 4 est disponible jusqu'à 8 Go de RAM. Ce n'est pas une Ferrari, mais il me parait suffisant pour une exploitation dans un cadre pédagogique. 

J'ai lu quelques textes sur la façon d'assembler des clusters avec Raspberry, pour la solution Hadoop + Spark - et j'ai commencé avec un cluster de raspberry pi 3. celui-ci était un peu limité.

Puis j'ai décidé d'ajouter des Raspberry Pi 4 ce qui m'a permis d'inclure d'autre modules comme spark, cassandra...

Le résultat fonctionne et sa performance me permet de mener des TPs. 

## 2. Assemblage du cluster

Cette première partie vous guidera dans l'assemblage du cluster physique, l'installation du serveur Ubuntu 20.04 et la configuration de l'environnement pour le cluster. 

### 2.1 De quoi avez-vous besoin ?

Nous avons monté 2 clusters un premier de base avec 4 raspberry pi 3 remplacé par des raspberry pi 4 et un plus grand cluster composé de 22 raspberry pi 4 et de 10 raspberry pi 3.

Nous donnerons les explications pour le cluster composé de 4 raspberry pi 4. 

### 2.1.1 Matériel utilisé

* Cluster de base 

	* 4 Raspberry Pi 4 4 Go 
	* 1 switchs 5 ports gigabit (10/100/1000)(Netfear GS 205)
	* 4 alimentations USB c, 15W pour raspberry pi 4
	* 4 cartes micro SD 32 GB (SanDisk Edge) 
	* 4 câbles 25cm Ethernet pour coonecter les raspberri au switch
	* 1 câble ethernet 3m 
	* 1 MakerFun pour Raspberry Pi 4 Model B + Boîtier avec Ventilateur et radiateur en Acrylique en Couches superposables
	* 2 multiprises 5 prises (seuls 3 chargeurs peuvent être branchés par multiprise) avec un bouton on/off

* Cluster mixte

	* 22 Raspberry Pi 4 4 Go 
	* 10 Raspberry Pi 3 1 Go
	* 8 switchs 5 ports gigabit (10/100/1000)
	* 1 switch 16 ports (10/100/1000)
	* 20 alimentations USB c, 15W pour raspberry pi 4
	* 32 Cartes micro SD pour vos raspberry
	* 1 câble ethernet 3m
	* 40 Câbles 25cm  Ethernet pour la mise en réseau
	* 3 Alimentation 4 ports USB pour les raspberry pi 3
	* 8 MakerFun pour Raspberry Pi 4 Model B + Boîtier avec Ventilateur et radiateur en Acrylique en Couches superposables
	* 12 multiprises 5 prises (seuls 3 chargeurs peuvent être branchés par multiprise) avec un bouton on/off



#### 2.1.2 Quelques explications sur le matériel :

Le Raspberry Pi 4 dispose du wifi et d'un Ethernet gigabit. J'ai opté par un réseau câblé pour la communication en cluster, en utilisant le commutateur gigabit. J'utilise également le wifi pour l'accès à distance. Ainsi, vous devriez utiliser des câbles cat 6.

L'achat de cartes SD de bonne qualité avec une vitesse de lecture/écriture élevée est essentiel pour les performances du cluster. 
Il est possible d'améliorer les performances en branchant une carte ssd via le port usb c [].


J'ai utilisé les guides suivants [2, 3, 4, 5] :

* [Building a Raspberry Pi Hadoop / Spark Cluster](https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2)


* [Build Raspberry Pi Hadoop/Spark Cluster from scratch](https://medium.com/analytics-vidhya/build-raspberry-pi-hadoop-spark-cluster-from-scratch-c2fa056138e0)

	
* [Building a Hadoop cluster with Raspberry Pi - IBM Developer Recipes](https://developer.ibm.com/recipes/tutorials/building-a-hadoop-cluster-with-raspberry-pi/)

* [Raspberry PI Hadoop Cluster](http://www.widriksson.com/raspberry-pi-hadoop-cluster/) Ce lien m'avait permis de construire m'ont premier cluster hadoop sous raspberry pi 3. 

Afin de vous aider lors de la lecture de ce tutoriel, vous retrouverez les différents fichiers de configuration dans une structure de dossiers similaire à celle qui existe dans les raspberry (attention  - les IP, les noms de serveurs, etc., sont très certainement différents pour vous). 

Tous les fichiers sont dans la version finale, avec des versions distribuées de Hadoop, Spark.

### 2.2 Montage du cluster

La première étape consiste au montage des boitiers avec les raspberry, de relier les alimentations, les cables réseaux.
 

### 2.3 Installation d'un système opérationnel

Tout d'abord, vous devez assembler les éléments physiques dans le support du cluster, moins les cartes SD. 


Mon ordinateur portable fonctionne sous mac os X - et j'utilise régulièrement le terminal et brew ou apt-get. 


#### 2.3.1 Télécharger et installer l'imageur Raspberry Pi

Le meilleur outil pour créer la carte micro SD avec le serveur Ubuntu est le [Raspberry Pi Imager](https://www.raspberrypi.org/software/) [5]. L'outil est disponible pour Windows, Ubuntu et Mac.

Cet utilitaire gravera votre système d'exploitation initial en version vierge.

J'ai essayé d'utiliser cet adaptateur microSD vers SD bon marché qui arrive généralement avec la carte micro SD dans l'emplacement SD de l'ordinateur portable. C'est un peu lent.

Le Raspberry Pi 4 a une architecture 64 bits. Le Raspberry pi 3 possède une architecture 32 bits. 

Lors de mes premières tentatives, j'ai utilisé le Raspbian (seule la version 32 bits disponible) - mais j'ai eu des problèmes avec l'installation de Spark.

J'ai décidé, après lecture de quelques tutoriels,  d'utiliser la version Ubuntu 64 bits (recommandée par Ubuntu pour Pi 4) (et la version 32 bits pour les Pi 3).

* **Initialisation des SD**

Insérez votre SD et démarrez l'imageur Raspberry Pi et installez le serveur Ubuntu 20.04 64bit. 
Faites de même pour toutes vos cartes PI Micro SD (pour les raspberry pi 4)

Le serveur Ubuntu 20.04 est disponible en version minimale, configuré pour connecter le réseau Ethernet par DHCP.


#### 2.3.2 Connexion au réseau

Il s'agit d'un cluster - le réseau est primordial. Tout ce tutoriel suppose que vous avez un réseau domestique avec un routeur ou une passerelle.


Vous aurez besoin d'accéder au système d'exploitation pour configurer votre réseau. 

Vous pouvez le faire de deux façons différentes : 

* La première façon, la plus simple est d'acheter un adaptateur du micro-HDMI au HDMI, un clavier filaire et de brancher votre Raspberry un par un. Vous aurez un accès direct avec le nom d'utilisateur/mot de passe initial.

* La deuxième façon de connecter initialement les raspberry est de compter sur votre DHCP et de connecter le Pi sur votre réseau câblé (ethernet).

Mon serveur dhcp domestique contenait les numéros ip et les noms qui seront utilisé par chaque raspberry pi. Cela m'a permis lors du démarrage des raspberry pi de tomber sur les bons couples nom/ip.

Dans mon cas, un rapide coup d'oeil sur le serveur dhcp (un nas synology) et/ou l'utilisation Superscan m'ont permis de connaître le numéro ip de chaque nouvel arrivant (démarrer les raspberry pi successivement). je me suis connecté via ssh à chaque raspberry.

Par exemple : 

```
ssh ubuntu@pi-node13
```

L'utilisateur/mot de passe par défaut est ubuntu/ubuntu, et il vous sera demandé de changer le mot de passe lors de la première connexion. 
J'ai changé les mots de passe en « raspberry ». Il s'agit d'un laboratoire, évitez d'utiliser vos vrais mots de passe dans le cluster. Une fois le mot de passe changé le raspberry efectuera un `reboot` il faudra se reconnecter.


Mettez sous tension un seul Raspberry à la fois, configurez son réseau, son nom d'hôte, ses hôtes et son utilisateur et baissez-le. Cela facilitera l'identification de l'IP dynamique pour la connexion initiale avec ssh.

Lorsque vous mettez un Pi 4 sous tension, vous verrez une LED rouge et verte clignoter près du micro SD. La LED rouge est alimentée et le vert montre qu'il accède à votre mémoire secondaire (le micro SD).
Tous mes Pi ont la même configuration pour l'emplacement de l'utilisateur/mot de passe et des fichiers. Cela facilite la gestion du cluster.

#### 2.3.3 La première tâche consiste à configurer votre réseau.

Comme je l'ai écrit précédemment, j'ai décidé de configurer Ethernet. 

Le serveur Ubuntu 20.04 utilise netplan pour la configuration du réseau. 

Netplan modifiera ensuite vos paramètres réseau en conséquence.
Important - l'indentation doit avoir 4 espaces.

Vous trouverez le fichier suivant à modifier :
/etc/netplan/50-cloud-init.yaml

Vous pouvez copier mon fichier et le modifier en conséquence :

`/etc/netplan 50-cloud-init.yaml`

```
#Cluster configuration

network:
  version: 2
  ethernets:   
    eth0:
      dhcp4: false
      addresses: [192.168.0.113/24]
      gateway4: 192.168.0.255
      nameservers:
        addresses: [192.168.0.100,8.8.8.8]
```

Après avoir modifié le fichier, vous devez confirmer les modifications :

```
ubuntu@ubuntu :/etc/netplan$ sudo netplan apply`
```

Vous devez adapter le fichier à votre environnement. Habituellement, il vous suffira de décider des adresses IP du cluster, de changer l'adresse IP du routeur (passerelle).

| Nom d'hôte | IP (Ethernet) |
| ------- | ------ | ------ |
| pi-node13 | 192.168.0.113 |
| pi-node14 | 192.168.0.114 |
| pi-node15 | 192.168.0.115 |
| pi-node16 | 192.168.0.116 |

Remarque - assurez-vous de supprimer la plage que vous avez choisie de la plage que votre routeur peut utiliser pour les connexions DHCP.

Une fois que vous avez des connexions réseau stables, vous pouvez démarrer la configuration réelle. Gardez à l'esprit que le cluster utilise des connexions réseau, les droits d'accès doivent être tous corrects entre les raspberry, sinon vos services distribués échoueront.



### 2.4 Créez vos utilisateurs

Vous allez créer le même utilisateur dans tous les nœuds, avec un accès sudo :

Remarque - n'utilisez pas la commande useradd de bas niveau !

`sudo adduser pi`


    sudo usermod -aG sudo pi
    sudo usermod -aG admin pi

Les commandes *usermod* assurent l'accès à *sudo*.

Connectez-vous en tant que pi et mettez à jour votre système !

    sudo apt
    sudo apt update
    sudo apt upgrade

Vous trouverez utile d'installer le paquet net-tools ! Il est livré avec *netstat*, et nous l'utiliserons après l'utiliser pour vérifier les services actifs (ports) dans les nœuds :

    sudo apt-get install net-tools
    sudo apt install python3 python-is-python3
    sudo apt install python3-pip

### 2.5 accès au bureau à distance

J'ai égalemebt installé une interface graphique légère (xfce4) avec un navigateur Web (chromium) et un accès au bureau à distance (xrdp). 

Dans mon cas, ce n'est pas nécessaire car je me connecte via *ssh* et que je fais tout via un terminal. Mais il arrive qu'il soit nécessaire de brancher un clavier, une souris et un écran.

Vous pouvez choisir n'importe quelle interface graphique.


Afin d'activer l'accès au bureau à distance, vous devez :

Installez xfce4 et xrdp :
      
     sudo apt-get install xfce4
     sudo apt-get install xrdp
     
créez le fichier  /home/pi/.xsession

    echo xfce4-session > /home/pi/.xsession

et modifiez le fichier /etc/xrdp/startwm.sh

    sudo nano /etc/xrdp/startwm.sh
    
en ajoutant ce qui suit à la fin :

    startxfce4
    
Redémarrez les services :

    sudo service xrdp restart

On peut installer chrome :

    sudo apt-get install chrome-browser

Juste au cas où, installez le support extFat  :

    sudo apt install exfat-fuse
    

### 2.6 Configuration du hostname et des hosts

Vous devez mettre à jour le nom d'hôte et aussi les fichiers hôtes dans /etc. Voir les exemples dans GitHub.
Note - supprimer du fichier hôte la référence à localhost 127.0.01.

/etc/hosts

    # The following lines are desirable for IPv6 capable hosts
    ::1 ip6-localhost ip6-loopback
    fe00::0 ip6-localnet
    ff00::0 ip6-mcastprefix
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters
    ff02::3 ip6-allhosts

    192.168.0.113 pi-node13
    192.168.0.114 pi-node14
    192.168.0.115 pi-node15
    192.168.0.116 pi-node16


/etc/hostname

    pi-node13

### 2.7 Installation de Java

C'était un talon d'Achille :
Hadoop est compilé et fonctionne bien sur Java8. Je l'ai cherché, mais je n'ai pas trouvé de build de Java Hotspot 8 ou Oracle Java 8 pour l'architecture AMR64. La solution retenu par la communauté est d'utiliser l'OpenJDK8, déjà disponible dans les référentiels Ubuntu.

Vous trouverez des informations sur le support Hadoop et Java dans [6] :

Pour installer java :

    sudo apt-get install openjdk-8-jdk
    
Voici ma version :

    pi@pi-node13:~$ java -version
    openjdk version "1.8.0_275"
    OpenJDK Runtime Environment (build 1.8.0_275-8u275-b01-0ubuntu1~20.04-b01)
    OpenJDK 64-Bit Server VM (build 25.275-b01, mixed mode)


### 2.8 Configuration de SSH

Modifier le fichier  : home/pi/.ssh/config pour créer des raccourcis pour ssh

    Host pi-node13
    User pi
    Hostname 192.168.0.113

    Host pi-node14
    User pi
    Hostname 192.168.0.114

    Host pi-node15
    User pi
    Hostname 192.168.0.115

    Host pi-node16
    User pi
    Hostname 192.168.0.116



Générer une paire de clés rsa publiques/privées pour l'utilisateur pi dans tous les nœuds du cluster :

Example de Commandes et sorties attendues :

    pi@pi-node13:~$  ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/pi/.ssh/id_rsa):
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/pi/.ssh/id_rsa
    Your public key has been saved in /home/pi/.ssh/id_rsa.pub
    The key fingerprint is:
    SHA256:mKDvp5u/AsK5CxUUYdkFNSM+rSI4S4aQJR7Wd1AcPZU pi@pi1
    The key's randomart image is:
    +---[RSA 3072]----+
    |.oB=o=Ooo ...    |
    |o*oo.+ = o E     |
    |o.. = o   .      |
    |+  o + o         |
    |*o= . o S        |
    |+B.o             |
    |o....            |
    |.. ....          |
    | .. =*o.         |

Copiez les clés publiques dans la liste des clés autorisées :

`cat .ssh/id_rsa.pub >> .ssh/authorized_keys`

Et copiez sur tous les nœuds :

`cat ~/.ssh/id_rsa.pub | ssh pi2 'cat >> .ssh/authorized_keys'`
`cat ~/.ssh/id_rsa.pub | ssh pi3 'cat >> .ssh/authorized_keys'`

Remarque - vous devez effectuer ce processus dans chaque nœud de cluster. En fin de compte, tous les nœuds auront toutes les clés publiques dans leurs listes. C'est important - ne pas avoir la clé ce qui empêcherait la communication de machine à machine après.


### 2.9 Scripts pour gérer le cluster

Créez des fonctions pour vous aider dans la gestion du cluster, en ajoutant ce qui suit dans le fichier suivant :

/home/pi/.bashrc


    ####### functions  for the cluster management

    function otherpis {
      grep "pi" /etc/hosts | awk '{print $2}' | grep -v $(hostname)
    }

    function clustercmd {
      for pi in $(otherpis); do ssh $pi "$@"; done
      $@
    }

    function clustercmd-sudo {
      for pi in $(otherpis); do ssh $pi "echo pi| sudo -S  $@"; done
      echo pi| sudo -S $@
    }

    function clusterreboot {
      clustercmd-sudo shutdown -r now
    }

    function clustershutdown {
      clustercmd-sudo shutdown now
    }

    function clusterscp {
      for pi in $(otherpis); do
        cat $1 | ssh $pi "sudo tee $1" > /dev/null 2>&1
      done
    }

exécutez la commande :

`source /home/pi/.bashrc`

Vous devez le faire dans tous les nœuds. Utilisez *scp* pour copier entre les nœuds si vous préférez.

### 2.10 Synchronisation de l'heure

Habituellement, je synchronise toutes mes machines avec un serveur de temps en UTC. Dans un cluster, c'est encore plus important.

    pi@pi-node13:~$ clustercmd date
    Sat Jan 23 20:59:28 UTC 2021
    Sat Jan 23 20:55:30 UTC 2021
    Sat Jan 23 20:53:31 UTC 2021
    Sat Jan 23 20:52:31 UTC 2021


Exécutez la commande suivante :

    clustercmd-sudo apt install htpdate -y
    clustercmd-sudo htpdate -a -l www.pool.ntp.org

Cette dernière commande utilise la date *htpdate* pour synchroniser les horloges des nœuds avec le serveur [www.pool.ntp.org](https://www.ntppool.org/fr/).



[1] P. G. Taranti. [https://github.com/ptaranti/RaspberryPiCluster](https://github.com/ptaranti/RaspberryPiCluster), consulté le 27/01/2021

[2] A. W. Watson. [Building a Raspberry Pi Hadoop / Spark Cluster (2019)](https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2), consulté le 27/01/2021

[3] W. H. Liang. [Build Raspberry Pi Hadoop/Spark Cluster from scratch (2019)](https://medium.com/analytics-vidhya/build-raspberry-pi-hadoop-spark-cluster-from-scratch-c2fa056138e0), consulté le 27/01/2021

[4] A. Verdugo. [Building a Hadoop cluster with Raspberry Pi: Installing, configuring and testing a distributed storage and processing cluster with single-board computers](https://developer.ibm.com/recipes/tutorials/building-a-hadoop-cluster-with-raspberry-pi/) (2017), consulté le 27/01/2021

[5] G. Hollingworth. [Introducing Raspberry Pi Imager, our new imaging utility ](https://www.raspberrypi.org/blog/raspberry-pi-imager-imaging-utility/)(2020), consulté le 27/01/2021

[6] A. Ajisaka. [Hadoop Java Versions](https://cwiki.apache.org/confluence/display/HADOOP/Hadoop+Java+Versions) (2020), consulté le 27/01/2021

[6]J. Widriksson. [Raspberry PI Hadoop Cluster](http://www.widriksson.com/raspberry-pi-hadoop-cluster/) (2014), consulté le 27/01/2021