import json
import requests
from io import StringIO  # python3 (or BytesIO for python2)
import boto3

def lambda_handler(event, context):
    # TODO implement
    base_url = "https://data.alpaca.markets/"

    parameters =  {"start": "2021-04-01T0:00:00Z", 
                "end": "2021-08-26T11:00:00Z", "timeframe": "1Day" }
    
    headers = {"Apca-Api-Key-Id": "PKF2QMR530IM4SKCFZ68", "Apca-Api-Secret-Key": "4BGfZRQbMFZ67U0x5M8bayTUgUcP1qpK6lfdq1Zd"}
    response = requests.get(url=base_url + "v2/stocks/AAPL/bars?", headers=headers, params=parameters)
    print(response)
    print(response.json())
    bucket = 'cloudcasa'  # already created on S3
    csv_buffer = StringIO(str(response.json()))
    #df.to_csv(csv_buffer)

    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, 'df.json').put(Body=csv_buffer.getvalue())
    
    return {
        'statusCode': 200,
        'body': response.json()
    }