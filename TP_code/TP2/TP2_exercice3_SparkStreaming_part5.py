import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        sc = SparkContext(appName="StreamingreduceByKeyAndWindow");
        # 2 is the batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        # Checkpoint
        ssc.checkpoint("file:///tmp/spark")

        # Definition du socket 
        # Récupération du texte
        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))


        # Comptage de la chaine  de caractères ERROR
        ## Split la ligne
        ## filter en ne retenant que Error dans les splits
        ## puis les compter en cumulant


        ## summary function
        ## reverse function
        ## window size = 10
        ## sliding interval = 2
        counts = lines.flatMap(lambda line: line.split(" "))\
                    .filter(lambda word:"ERROR" in word)\
                    .map(lambda word : (word, 1))\
                    .reduceByKeyAndWindow(lambda x, y: int(x) + int(y), lambda x, y: int(x) - int(y), 10, 2)

        ## Display the counts
        ## Start the program
        ## The program will run until manual termination
        counts.pprint()
        ssc.start()
        ssc.awaitTermination()