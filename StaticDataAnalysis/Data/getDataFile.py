import json
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
    data_df = pd.read_json(data)
    return data_df