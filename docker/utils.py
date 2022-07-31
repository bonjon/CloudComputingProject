import pandas as pd
import yaml
import boto3
from configuration import *
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_bucket(news=False):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    logger.info("Bucket '%s' created successfully", bucket.name)
    return bucket


def list_s3(bucket, prefix=None):
    """
    Lists the objects in a bucket, optionally filtered by a prefix.

    :param bucket: The bucket to query.
    :param prefix: When specified, only objects that start with this prefix are listed.
    :return: The list of objects.
    """
    try:
        if not prefix:
            objects = list(bucket.objects.all())
            logger.info("Returning all objects inside the bucket")
        else:
            objects = list(bucket.objects.filter(Prefix=prefix))
            logger.info("Returning objects with prefix: %s", prefix)
            logger.info(
                "Got objects %s from bucket '%s'", [o.key for o in objects], bucket.name
            )
    except ClientError:
        logger.exception("Couldn't get objects for bucket '%s'", bucket.name)
        raise
    else:
        return objects


def get_df(bucket, option) -> pd.DataFrame:
    df_list = []
    logger.info("Getting data from S3 bucket")
    if option == "news":
        for obj in list_s3(bucket, prefix=option):
            data = yaml.load(obj.get()["Body"].read(), Loader=yaml.FullLoader)
            df_list.append(pd.DataFrame.from_dict(data["news"]))
    else:
        for obj in list_s3(bucket, prefix=str(SYMBOLS[option])):
            data = yaml.load(obj.get()["Body"].read(), Loader=yaml.FullLoader)
            df_list.append(pd.DataFrame.from_dict(data["bars"]))
    logger.info("Got %d dataframe from S3 bucket", len(df_list))
    return pd.concat(df_list)


def RSI(close, n=14):
    delta = close.diff()
    delta = delta[1:]
    pricesUp = delta.copy()
    pricesDown = delta.copy()
    pricesUp[pricesUp < 0] = 0
    pricesDown[pricesDown > 0] = 0
    rollUp = pricesUp.rolling(n).mean()
    rollDown = pricesDown.abs().rolling(n).mean()
    rs = rollUp / rollDown
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi
