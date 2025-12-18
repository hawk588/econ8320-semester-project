import requests
import json
import pandas as pd
import os
from datetime import date

seriesIds = ['LNS14000000','CES0000000001','CUUR0000SA0','WPUFD49207']
api_key = os.getenv('API_KEY', None) 

def initBlsData(): 
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": seriesIds,"startyear":date.today().year - 5, "endyear":date.today().year, "registrationkey":api_key})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    for series in json_data['Results']['series']:
        x = pd.DataFrame(columns = ['id', 'year', 'period', 'value', 'footnotes'])
        seriesId = series['seriesID']
        for item in reversed(series['data']):
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes=""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
        
            if ('M01' <= period <= 'M12') and value != '-':
                x.loc[len(x)] = [seriesId,year,period,value,footnotes[0:-1]]

        x.to_csv("data/" + seriesId + ".csv", index=False)

def updateBlsData():
    for seriesId in seriesIds:
        x = pd.read_csv("data/" + seriesId + ".csv")
        lastPeriod = x.period[len(x) - 1]
        lastYear = x.year[len(x) - 1]
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": [seriesId],"startyear":str(lastYear), "endyear":date.today().year, "registrationkey":api_key})
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
        json_data = json.loads(p.text)
        foundNew = False
        for item in reversed(json_data['Results']['series'][0]['data']):
            year = item['year']
            period = item['period']
            foundNew = int(year) > lastYear or (int(year) == lastYear and period > lastPeriod)
            if foundNew:
                value = item['value']
                footnotes=""
                for footnote in item['footnotes']:
                    if footnote:
                        footnotes = footnotes + footnote['text'] + ','
            
                if 'M01' <= period <= 'M12' and value != '-':
                    x.loc[len(x)] = [seriesId,year,period,value,footnotes[0:-1]]

        x.to_csv("data/" + seriesId + ".csv", index=False)

initBlsData()
updateBlsData()