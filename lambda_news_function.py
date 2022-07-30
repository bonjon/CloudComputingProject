import boto3
import json
import logging
import os
import requests
from datetime import date, timedelta
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    headers = {'APCA-API-KEY-ID' : os.environ['APCA_API_KEY_ID'], 'APCA-API-SECRET-KEY' : os.environ['APCA_API_SECRET_KEY']}
    parameters = {"start": event['start'], "symbols": event['symbols'],"limit": event['limit'], "sort": event['sort']}

    api_response = requests.get("https://data.alpaca.markets/v1beta1/news?", params=parameters, headers=headers)
    
    if api_response.status_code != 200:
        logger.error('error' + str(api_response.status_code) + 
                    'for API request')

    bucket_name = os.environ['BUCKET_NAME']
    body = json.dumps(api_response.json())
    file_name = "news.json"
    s3_response = s3.put_object(Body = body, Bucket = bucket_name, Key = file_name)

    if s3_response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('error' + s3_response['ResponseMetadata']['HTTPStatusCode'] + 
                    'while uploading json to s3')

    return {
        "statusCode": 200,
        "body": "OK for query: "
        + str(event["symbols"])
        + " from: "
        + str(event["start"]),
    }