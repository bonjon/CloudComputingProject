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
    resp = s3.list_objects_v2(Bucket = os.environ['BUCKET_NAME'], Prefix = event['symbol'])

    start_date = event['start']
    file_name = event['symbol'] + '.json'
    
    if resp['KeyCount'] > 0:
        start_date = str(date.today() - timedelta(days = 7))
        file_name = event['symbol'] + start_date + '.json'

    headers = {'APCA-API-KEY-ID' : os.environ['APCA_API_KEY_ID'], 'APCA-API-SECRET-KEY' : os.environ['APCA_API_SECRET_KEY']}
    parameters = {'start' : start_date + 'T0:00:00Z', 'timeframe' : event['timeframe']}

    api_response = requests.get(event['base_url'] + event['sub_url'] + event['symbol'] + event['query_url'],
        headers = headers,
        params = parameters)
    
    if api_response.status_code != 200:
        logger.error('error' + str(api_response.status_code) + 
                    'for API request' + event['base_url'] + 
                    event['sub_url'] + event['symbol'] + event['query_url'])

    bucket_name = os.environ['BUCKET_NAME']
    body = json.dumps(api_response.json())
    
    s3_response = s3.put_object(Body = body, Bucket = bucket_name, Key = file_name)

    if s3_response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('error' + s3_response['ResponseMetadata']['HTTPStatusCode'] + 
                    'while uploading json to s3')

    return {
        "statusCode": 200,
        "body": "OK for query: "
        + str(event["symbol"])
        + " from:"
        + str(event["start"])
        + " in:"
        + str(event["timeframe"]),
    }