
# Importation des librairies
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        # Demarrer ParkContext
        sc = SparkContext(appName="StreamingErrorCount");
        # Demarrer Context Streaming
        # 2 is the batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        # Creation du checkpoint
        ssc.checkpoint("file:///tmp/spark")

        # Definir le socket où le système lit
        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))


        # Function permettant la mise a jour des comptes
        def countWords(newValues, lastSum):
            if lastSum is None :
                lastSum = 0
            return sum(newValues, lastSum)

        # 
        word_counts = lines.flatMap(lambda line: line.split(" "))\
                    .map(lambda word : (word, 1))\
                    .updateStateByKey(countWords)

        ## Affichage des couples mts-nombre
        ## Start the program
        ## The program will run until manual termination
        word_counts.pprint()
        ssc.start()
        ssc.awaitTermination()