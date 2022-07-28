import boto3
import json
import logging
import os
import requests
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    headers = {'APCA-API-KEY-ID' : os.environ['APCA_API_KEY_ID'], 'APCA-API-SECRET-KEY' : os.environ['APCA_API_SECRET_KEY']}
    parameters = {'start' : event['start'], 'timeframe' : event['timeframe']}

    api_response = requests.get(event['base_url'] + event['sub_url'] + event['symbol'] + event['query_url'],
        headers = headers,
        params = parameters)
    
    if api_response.status_code != 200:
        logger.error('error' + str(api_response.status_code) + 
                    'for API request' + event['base_url'] + 
                    event['sub_url'] + event['symbol'] + event['query_url'])

    s3 = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']
    file_name = event['symbol'] + '.json'
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