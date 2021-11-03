import warnings
import json
warnings.filterwarnings('ignore')

# read file
with open('data/streaming_data_analysis.json', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)