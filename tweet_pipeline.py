import os
import tweepy as tw
import pandas as pd
from tqdm import tqdm, notebook
import os

def searchtweets_wirte(query, start_time, end_time, file_name, client):
    completed = False
    while not completed:
        # if file exist, we get update the end_time, as tweepy read in desceding time order
        if os.path.isfile(file_name):
            # preprocess from last checkpoint, we continue reading from last end_time
            last_read = pd.read_csv('last_read.csv', index_col=0)
            last_date = last_read['created_at'].item()
            temp = last_date.split('+')[0].split()
            end_time = temp[0]+'T'+temp[1]+'Z'
            # stop when we have completed the data pipeline
            if temp[0]==start_time.split('T')[0]:
                completed = True
                print('Pipeline Completed')
                return 
        # get recent matching tweets according to the query
        tweets = client.search_recent_tweets(query=query, 
                                             max_results=100,
                                             user_fields = ['username', 'public_metrics', 'description', 'location'],
                                             tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
                                             expansions = 'author_id',
                                             start_time = start_time,
                                             end_time = end_time)

        result = []

        # we firstly map each user_id to an index which allows us to locate the user
        users = tweets.includes['users']
        user_dict = {}
        for i, user in enumerate(users):
            user_dict[user.id] = i

        # then we collect all tweets info
        for tweet in tweets.data:
            # for each tweet, find the author
            user_index = user_dict[tweet.author_id]
            user = users[user_index]
            tweet_dict = { 'author_id': tweet.author_id, 
                           'username': user.username,
                           'author_followers': user.public_metrics['followers_count'],
                           'author_tweets': user.public_metrics['tweet_count'],
                           'author_description': user.description,
                           'author_location': user.location,
                           'text': tweet.text,
                           'created_at': tweet.created_at,
                           'retweets': tweet.public_metrics['retweet_count'],
                           'replies': tweet.public_metrics['reply_count'],
                           'likes': tweet.public_metrics['like_count'],
                           'quote_count': tweet.public_metrics['quote_count']}
            # append current tweet's dictionary to the result list
            result.append(tweet_dict)

        df_tweet = pd.DataFrame(result)
        
        
        # if file does not exist write header 
        if not os.path.isfile(file_name):
            df_tweet.to_csv(file_name, index=False)
            (df_tweet.tail(1)).to_csv('last_read.csv', index=False)
        else: # else it exists so append without writing the header
            # append to the vaccine csv file
            df_tweet.to_csv(file_name, mode='a', index=False)
            # overwrite the last_read csv file
            (df_tweet.tail(1)).to_csv('last_read.csv', mode='w+', index=False)