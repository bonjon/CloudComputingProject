import pandas as pd
import requests

endpoint = 'https://api.twitter.com/2/tweets/search/recent'
headers = {'Authorization' : 'Bearer AAAAAAAAAAAAAAAAAAAAAGaVfQEAAAAAw0NVD2QK7d%2Boe%2B1EyKFZpWs%2F0rA%3DlzUkkQ4W5Eirk1c9k97CyybihOe83XrUaqnPgkRd8T8M3YorMc'}
parameters = {'query' : 'microsoft', 'max_results' : '100', 'tweet.fields' : 'lang'}

response = requests.get(endpoint, headers = headers, params = parameters)
tweets = response.json()['data']
next_token = response.json()['meta']['next_token']
parameters['next_token'] = next_token

response_page2 = requests.get(endpoint, headers = headers, params = parameters)
tweets += response_page2.json()['data']

#for tweet in tweets[:]:
#    if tweet['lang'] != 'en':
#        tweets.remove(tweet)

#tweet_list = []

for tweet in tweets:
    print(tweet)

#for tweet in tweets[:]:
#    tweet_list.append(tweet['text'])

#for tweet in tweet_list:
#    print(tweet)