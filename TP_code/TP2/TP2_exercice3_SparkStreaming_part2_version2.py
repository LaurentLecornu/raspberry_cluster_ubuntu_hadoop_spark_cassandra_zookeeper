import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

def createContext(host, port):
    sc = SparkContext(appName="SparkStreamingExercice3");

    # 10 la duree de l’interval : 10 secondes
    ssc = StreamingContext(sc,10)



    # Lines n’est pas un rdd mais une suite de rdd, not statique, changeant constamment
    # Update function
    def countWords(newValues, lastSum):
        if lastSum is None :
            lastSum = 0
        return sum(newValues, lastSum)


    lines = ssc.socketTextStream(host,port)
    # Que sont les valeurs de sys.argv[1] et sys.argv[2]
    # Comptage
    
    # for line in lines:
    # print(lines)
   
    counts = lines.flatMap(lambda line: line.split(" "))\
                  .map(lambda word: (word, 1))\
                  .updateStateByKey(countWords)
    # print en streaming
    counts.pprint()
    return ssc

# Begin
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: firstStreamApp.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    host, port = sys.argv[1:]
    
    ssc = StreamingContext.getOrCreate("./checkpointL", lambda: createContext(host, int(port)))

    ssc.start() 
    ssc.awaitTermination()

