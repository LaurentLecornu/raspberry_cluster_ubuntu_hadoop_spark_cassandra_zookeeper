import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Begin
if __name__ == "__main__":
        sc = SparkContext(appName="StreamingreduceByWindow");
        # 2 is the batch interval : 2 seconds
        ssc = StreamingContext(sc, 2)

        ssc.checkpoint("file:///tmp/spark")

        lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

        ## summary function
        ## reverse function
        ## window size = 10
        ## sliding interval = 2
        ## Attention seuls des nombres sont écrits
        sum = lines.reduceByWindow(
                lambda x, y: int(x) + int(y),
                lambda x, y: int(x) - int(y),
                10,
                2
        )

        ## Display the counts
        ## Start the program
        ## The program will run until manual termination
        sum.pprint()
        ssc.start()
        ssc.awaitTermination()