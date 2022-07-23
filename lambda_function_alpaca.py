from io import StringIO  # python3 (or BytesIO for python2)
import boto3
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit


def lambda_handler(event, context):

    api = REST("PKF2QMR530IM4SKCFZ68", "4BGfZRQbMFZ67U0x5M8bayTUgUcP1qpK6lfdq1Zd")
    data = api.get_bars(
        [
            "AAPL",
            "AMZN",
            "GOOG",
            "MSFT",
            "TSLA",
            "NFLX",
            "META",
            "BABA",
            "TWTR",
            "KO",
            "NKE",
            "PYPL",
            "PEP",
            "UBER",
            "WMT",
        ],
        TimeFrame(1, TimeFrameUnit.Day),
        "2021-01-01",
        adjustment="raw",
    ).df

    bucket = "cloudcasa"  # already created on S3
    csv_buffer = StringIO()
    data.to_csv(csv_buffer)

    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket, "df.csv").put(Body=csv_buffer.getvalue())

    return {"statusCode": 200, "body": "OK"}
