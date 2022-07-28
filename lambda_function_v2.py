import boto3
import json
import os
import requests

def lambda_handler(event, context):
    headers = {'APCA-API-KEY-ID' : os.environ['APCA_API_KEY_ID'], 'APCA-API-SECRET-KEY' : os.environ['APCA_API_SECRET_KEY']}
    parameters = {'start' : event['start'], 'timeframe' : event['timeframe']}

    response = requests.get(event['base_url'] + event['sub_url'] + event['symbol'] + event['query_url'],
        headers = headers,
        params = parameters)
    
    s3 = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']
    file_name = event['symbol'] + '.json'
    body = json.dumps(response.json())
    
    s3.put_object(Body = body, Bucket = bucket_name, Key = file_name)

    return {
        "statusCode": 200,
        "body": "OK for query: "
        + str(event["symbol"])
        + " from:"
        + str(event["start"])
        + " in:"
        + str(event["timeframe"]),
    }