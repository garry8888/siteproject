from finance.models import Currency
import json
import requests

# api_spreadsheets gsx2json
# https://docs.google.com/spreadsheets/d/1BRDrKF9anTLPBBN5e3n_g2S0FTiiCFfPG5UuD2cnuPQ/edit?usp=sharing

# write currency catalogue in the model Currency
def json_get(path='http://gsx2json.com/api?id=1BRDrKF9anTLPBBN5e3n_g2S0FTiiCFfPG5UuD2cnuPQ&sheet=1'):
    response = requests.get(path)
    data_spreadsheet = json.loads(response.text)
    data_db = data_spreadsheet['rows']
    d = []
    
    for i in data_db:
        d.append(dict(
            name=i["название"],
            abbreviation=i["код10"],
            symbol=i["знак9"],
            index=i["index"]
        ))

    Currency.objects.bulk_create([Currency(**r) for r in d])