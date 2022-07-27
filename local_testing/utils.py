import os
from configuration import *
import yaml
import pandas as pd


def list_s3(path, prefix=None):
    if not prefix:
        objects = os.listdir(path)
    else:
        objects = [x for x in os.listdir(path) if prefix in x]
    return objects


def get_df(
    option,
) -> pd.DataFrame:
    df_list = []
    path = ".."
    for obj in list_s3(path, prefix=str(SYMBOLS[option])):
        with open(path + "/" + obj, "r") as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
            df_list.append(pd.DataFrame.from_dict(data["bars"]))

    return pd.concat(df_list)
