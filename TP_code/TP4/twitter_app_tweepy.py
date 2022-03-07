import tweepy

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAACKBZgEAAAAAc%2FO2ruLc9Itj4V%2B368cvau8Oas8%3DoXkYFvpB4e68UvykwmxrVOXpZAx2IgHjTcL5Pmbq67WGcvtUXT'
class IDPrinter(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        print(tweet)


printer = IDPrinter(BEARER_TOKEN)
printer.sample()

