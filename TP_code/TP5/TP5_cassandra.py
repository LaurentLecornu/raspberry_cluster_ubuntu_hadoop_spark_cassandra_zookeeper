from cassandra.cluster import Cluster
clstr=Cluster()

from cassandra.cluster import Cluster
clstr=Cluster()
session=clstr.connect("test")
#session.execute("create keyspace test with replication={'class': 'SimpleStrategy', 'replication_factor' : 1};")

qry='''    
CREATE TABLE test.kv (

    user text,
    title text ,
    uuid text,
    PRIMARY KEY(uuid)
);'''
DESCRIBE TABLE test.kv;

session.execute(qry)  
