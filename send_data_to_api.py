import requests
import pandas as pd
import os

TIME_CONSTANT = 'time'
API_URL = "https://arthur-tcc-api.herokuapp.com/street"
MAX_DATA_NUMBER = 10

def transform_in_seconds(val):
    return int(val.split(":")[1])*60+int(val.split(":")[2].split('.')[0])

for filename in os.listdir('csv/novas_leituras'):
    print('\n== reading file: '+filename)
    dados = pd.read_csv('csv/novas_leituras/'+filename)
    lat, lon = map(float, input("digite a latitude, longitude:").split(','))
    request_body = {
        'street_name': filename,
        'lat': lat,
        'long': lon,
        'data': []
    }

    dados['x'] = dados['x'].apply(float, 1)*9.8
    dados['y'] = dados['y'].apply(float, 1)*9.8
    dados['z'] = dados['z'].apply(float, 1)*9.8

    if TIME_CONSTANT in dados.columns:
        dados[TIME_CONSTANT] = dados[TIME_CONSTANT].apply(transform_in_seconds, 1)
        timeColumn = dados[TIME_CONSTANT]
        dados = dados.groupby(by=TIME_CONSTANT, axis=0).mean()

    for sequence, data in dados.iloc[:MAX_DATA_NUMBER].iterrows():
        request_data = {
            "num": sequence,
			"x_value": data['x'],
			"y_value": data['y'],
			"z_value": data['z']
        }

        request_body['data'].append(request_data)
    
    print(len(request_body['data']))
    r = requests.post(API_URL, request_body)
    print(r.content)
    