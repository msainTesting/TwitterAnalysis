import json
import warnings
warnings.filterwarnings("ignore")

def saveDataIntoFile(data):
    with open('data/staticDataAnalysis.json', 'w') as outfile:
         json.dump(data, outfile)
         return
