from pyspark.sql import SparkSession
import json
from pyspark.sql.types import *
from pyspark.sql.functions import udf, explode, lit, window


spark = SparkSession.builder.appName("Spark Structured Streaming from Kafka").getOrCreate()
sdfTweets = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "10.29.227.219:9092, 10.29.227.219:9093")\
.option("subscribe", "twitter_analysis_topic").option("startingOffsets", "latest")


spark.sparkContext.setLogLevel("ERROR")

def collapse(list,field):
	answer = []
	if(len(list)==0):
		return ["_"]
	for element in list:
		answer.append(element[field]) if field in element else "_"
	return answer

def processing_hashtags(s):
	data = json.loads(s)
	jsonhashtags = data["hashtag"]
	return list(map(lambda x:x.upper(),collapse(jsonhashtags,"text")))

processing_hashtags_udf = udf(lambda x: processing_hashtags(x), ArrayType(StringType()))

def processing_text(s):
	data = json.loads(s)
	return len(data["text"])

processing_text_udf = udf(lambda x: processing_text(x), IntegerType())

sdfTweets = sdfTweets.withColumn("hashtags",processing_hashtags_udf("value").cast("array<string>"))
sdfTweets = sdfTweets.withColumn("wordCount",processing_text_udf("value"))
sdfTweets = sdfTweets.drop("value")
sdfTweets = sdfTweets.withColumn("tweetCount",lit(1))
sdfTweets = sdfTweets.withColumn("hashtags", explode(sdfTweets["hashtags"].cast("array<string>")))
sdfTweets = sdfTweets.groupBy("hashtags", window(sdfTweets["timestamp"],"60 seconds","60 seconds")).sum("wordCount","tweetCount")
sdfTweets.writeStream.outputMode("update").foreach(processing_row).start().awaitTermination()
