import boto3
import json
import logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    count_endpoint = "https://api.twitter.com/2/tweets/counts/recent"
    search_endpoint = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization" : "Bearer " + os.environ["BEARER"]}
    parameters = {"query": event["query"]}
    s3 = boto3.client("s3")

    response = requests.get(count_endpoint, headers=headers, params=parameters)
    if response.status_code != 200:
            logger.error(
                "error "
                + str(response.status_code)
                + " for API request "
                + response.url
        )
    
    count = response.json()["data"]
    s3_response = s3.put_object(Body=json.dumps(count), Bucket=os.environ["BUCKET_NAME"], Key="count_tweet_" + event["query"] + ".json")
    if s3_response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        logger.error("error" + s3_response["ResponseMetadata"]["HTTPStatusCode"] + 
                    "while uploading count json to s3")

    parameters.update({"max_results": "100", "tweet.fields": "lang"})
    
    tweets = []
    for i in range(3):
        response = requests.get(search_endpoint, headers=headers, params=parameters)
        if response.status_code != 200:
            logger.error(
                "error "
                + str(response.status_code)
                + " for API request "
                + response.url
        )

        tweets += response.json()["data"]
        next_token = response.json()["meta"]["next_token"]
        parameters["next_token"] = next_token

    s3_response = s3.put_object(Body=json.dumps(tweets), Bucket=os.environ["BUCKET_NAME"], Key="search_tweet_" + event["query"] + ".json")
    if s3_response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        logger.error("error" + s3_response["ResponseMetadata"]["HTTPStatusCode"] + 
                    "while uploading json to s3")
    
    return {
        "statusCode": 200,
        "body": "Ok for query " + event["query"],
    }