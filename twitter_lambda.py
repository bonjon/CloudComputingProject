import boto3
import json
import logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    endpoint = 'https://api.twitter.com/2/tweets/search/recent'
    headers = {'Authorization' : 'Bearer ' + os.environ['BEARER']}
    parameters = {'query' : event['query'], 'max_results' : '100', 'tweet.fields' : 'lang'}

    response = requests.get(endpoint, headers = headers, params = parameters)
    tweets = response.json()['data']
    next_token = response.json()['meta']['next_token']
    parameters['next_token'] = next_token

    response_page2 = requests.get(endpoint, headers = headers, params = parameters)
    tweets += response_page2.json()['data']

    s3 = boto3.client('s3')
    s3_response = s3.put_object(Body = json.dumps(tweets), Bucket = os.environ['BUCKET_NAME'], Key = "tweet_" + event['query'] + '.json')

    if s3_response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('error' + s3_response['ResponseMetadata']['HTTPStatusCode'] + 
                    'while uploading json to s3')
    
    return {
        "statusCode": 200,
        "body": "Ok for query " + event['query'],
    }