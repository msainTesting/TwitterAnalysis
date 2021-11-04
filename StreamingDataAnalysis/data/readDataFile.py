import json
from heapq import merge

import pandas as pd
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_colwidth',0)

def loadDataFile(data):
    with open(data,'r') as json_file:
        data = json.load(json_file)
        for p in data:
            return p


def readDataWithPandas(data):
    data_df = pd.read_json(data, orient="columns")
    return data_df

def readMultipleDataWithPandas(data1):
    data_df1 = pd.read_json(data1, orient="values", lines=True)
    result = merge(data_df1)

    return result