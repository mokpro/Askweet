#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "131866583-DUasEYMwlQevDADf4a8E6KJKrgmpOsrDOp5L3276"
access_token_secret = "2tZo53FHQ22f3fDzxDgkS4Ai3xTsK16jixlVzxmmvzzMm"
consumer_key = "JgVBDjLUQV4NEAiHxUFIFhi3r"
consumer_secret = "0nRU7SFHxfSIuahHx2Df3z2OVg1HAybOP0o4u22bdNYdqkQobO"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['?','who', 'what', 'when', 'where', 'why', 'how', 'do', 'is', 'could', 'can', "can't", 'cant', 'would', "wouldn't", "wouldnt", 'should', "shouldn't", "shouldnt", 'did', 'will', 'has', 'have', "won't", 'does', 'wont', 'doesnt', "doesn\'t", 'had', 'are'])
