import json
import requests
from io import StringIO  # python3 (or BytesIO for python2)
import boto3
import os


def lambda_handler(event, context):
    base_url = "https://data.alpaca.markets/"
    parameters = {"start": "2021-01-01T0:00:00Z", "timeframe": "1Day"}

    headers = {
        "Apca-Api-Key-Id": os.environ["ApcaApiKeyId"],
        "Apca-Api-Secret-Key": os.environ["ApcaApiSecretKey"],
    }
    response = requests.get(
        url=base_url + "v2/stocks/AAPL/bars?", headers=headers, params=parameters
    )

    csv_buffer = StringIO(str(response.json()))

    s3_resource = boto3.resource("s3")
    s3_resource.Object(os.environ["bucketName"], "AAPL.json").put(
        Body=csv_buffer.getvalue()
    )

    return {"statusCode": 200, "body": "OK"}
