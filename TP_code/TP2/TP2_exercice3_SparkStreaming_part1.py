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
    ssc = StreamingContext(sc,5)


    # Lines n’est pas un rdd mais une suite de rdd, not statique, changeant constamment 

    lines = ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))
    # Que sont les valeurs de sys.argv[1] et sys.argv[2]
    # Comptage
    print(lines)
    counts = lines.flatMap(lambda line: line.split(" "))\
                  .map(lambda word: (word, 1))\
                  .reduceByKey(lambda x, y: x + y)
    # print en streaming
    counts.pprint()

    ssc.start() 
    ssc.awaitTermination()

