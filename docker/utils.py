import pandas as pd
import yaml
import boto3
from configuration import *


def get_bucket():
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)
    return bucket


def list_s3(bucket, prefix=None):
    """
    Lists the objects in a bucket, optionally filtered by a prefix.

    :param bucket: The bucket to query.
    :param prefix: When specified, only objects that start with this prefix are listed.
    :return: The list of objects.
    """
    # try:
    if not prefix:
        objects = list(bucket.objects.all())
    else:
        objects = list(bucket.objects.filter(Prefix=prefix))
        # logger.info("Got objects %s from bucket '%s'",
        # [o.key for o in objects], bucket.name)
    # except ClientError:
    # logger.exception("Couldn't get objects for bucket '%s'.", bucket.name)
    # raise
    # else:
    return objects


def get_df(bucket, option) -> pd.DataFrame:
    df_list = []
    for obj in list_s3(bucket, prefix=str(SYMBOLS[option])):
        data = yaml.load(obj.get()["Body"].read(), Loader=yaml.FullLoader)
        df_list.append(pd.DataFrame.from_dict(data["bars"]))

    return pd.concat(df_list)
