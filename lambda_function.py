import json
import requests
from io import StringIO  # python3 (or BytesIO for python2)
import boto3
import os


def lambda_handler(event, context):
    parameters = {"start": str(event["start"]), "timeframe": str(event["timeframe"])}

    headers = {
        "Apca-Api-Key-Id": os.environ["ApcaApiKeyId"],
        "Apca-Api-Secret-Key": os.environ["ApcaApiSecretKey"],
    }
    response = requests.get(
        url=str(event["base_url"])
        + str(event["sub_url"])
        + str(event["symbol"])
        + str(event["query_url"]),
        headers=headers,
        params=parameters,
    )

    csv_buffer = StringIO(str(response.json()))

    s3_resource = boto3.resource("s3")
    s3_resource.Object(os.environ["bucketName"], str(event["symbol"]) + ".json").put(
        Body=csv_buffer.getvalue()
    )

    return {
        "statusCode": 200,
        "body": "OK for query: "
        + str(event["symbol"])
        + " from:"
        + str(event["start"])
        + " in:"
        + str(event["timeframe"]),
    }
