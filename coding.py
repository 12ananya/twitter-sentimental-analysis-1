
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import numpy as np
import matplotlib.pyplot as plt
  
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'vcXfQlo2M4DAlYq0ChHTzw7kX'
        consumer_secret = 'wvb8PqkRUFK1GZPqjE1wu9QTIAGb6dEgGi5AyJ9ZXLCBVfNaie'
        access_token = '2485045476-MHgDn7EVwwU0fTE8u8wV45SRsXnwtcYZIjLovLX'
        access_token_secret = 'X5smgPs4eLlmgAyk7yTSe1Cf12cqMxxzsTmd5p8zZpcpY'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
        
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets(query='@PMOIndia' , count = 200)
    

  
    # picking positive tweets from tweets 
    np.ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(np.ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    np.ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(np.ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    np.netweets = [tweet for tweet in tweets if tweet ['sentiment']=='neutral']
    print("Neutral tweets percentage: {} %".format(100*len(np.netweets)/len(tweets)))
    positive=np.ptweets;
    negative=np.ntweets;
    neutral=np.netweets;
    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in np.ptweets[:20]: 
        print(tweet['text']) 
  
    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in np.ntweets[:20]: 
        print(tweet['text']) 
    
    # printing first 5 negative tweets
    print("\n\nNeutral tweets:") 
    for tweet in np.netweets[:20]: 
        print(tweet['text']) 
    a = format(100*len(np.ptweets)/len(tweets))
    b = format(100*len(np.ntweets)/len(tweets))
    c = format(100*len(np.netweets)/len(tweets))
    labels = 'Positive', 'Negative','Neutral'
    sizes = [a,b,c]
    colors = ['yellowgreen', 'lightskyblue','lightcoral']
    plt.pie(sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=90)
    
    
    plt.title('Narendramodi ')

    plt.axis('equal')
    plt.show()
        
    
if __name__ == "__main__": 
    # calling main function 
    main() 
