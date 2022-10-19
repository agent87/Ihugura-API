import requests
import json


class translator:
    api_url = "https://translate.googleapis.com/translate_a/single"
    client = "?client=gtx&dt=t"
    dt = "&dt=t"

    #fROM English to Kinyarwanda
    def to_rw(text):
        sl = "&sl=en"
        tl = "&tl=rw"
        r = requests.get(translator.api_url+ translator.client + translator.dt + sl + tl + "&q=" + text)
        return json.loads(r.text)[0][0][0]

    #From Kinyarwanda to English
    def to_en(text):
        sl = "&sl=rw"
        tl = "&tl=en"
        r = requests.get(translator.api_url+ translator.client + translator.dt + sl + tl + "&q=" + text)
        return json.loads(r.text)[0][0][0]


def trans_prediction(prediction):
    for index, answer in enumerate(prediction['answers']):
        print(answer['answer'])
        print(answer['context'])
        print('-----------------')
        #prediction['answers'][index]['answer'] = translator.to_rw(answer['answer'])
        #prediction['answers'][index]['context'] = translator.to_rw(answer['context'])
    
    return prediction