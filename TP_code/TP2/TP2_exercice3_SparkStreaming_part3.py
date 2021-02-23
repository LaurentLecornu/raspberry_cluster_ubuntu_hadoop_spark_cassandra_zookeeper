import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        sc = SparkContext(appName="StreamingcountByWindow");
        # batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        # Checkpoint
        ssc.checkpoint("file:///tmp/spark")


        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

        ## window size = 10, sliding interval = 2
        counts = lines.countByWindow(10, 2)

        ## Display the counts
        ## Start the program
        ## The program will run until manual termination
        counts.pprint()
        ssc.start()
        ssc.awaitTermination()