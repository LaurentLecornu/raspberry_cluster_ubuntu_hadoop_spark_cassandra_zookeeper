import tweepy
import json

from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
from random import choice
from time import sleep

consumer_key=" "
consumer_secret=" "

access_token=" "
access_token_secret=" "

producer = KafkaProducer(bootstrap_servers=["10.29.227.219:9092"])

class StreamListener(Stream):
    def on_data(self, data):
        tweet_info = json.loads(data)
        print(tweet_info['text'])
        # on peut encoder  une  partie de json
        producer.send("twitter_analysis_topic", data)

stream = StreamListener(consumer_key, consumer_secret,access_token, access_token_secret)

stream.filter(track=["ukrain"])
