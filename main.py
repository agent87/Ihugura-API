from flask import Flask, request
from packages import pindo
import json


try:
    with open('/etc/config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {}


app = Flask(__name__)
#Import Config
app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')


#INDEX
@app.get("/")
def root():
    return {"Hello": "World"}

#SPEECH ENABLED QUERY KINYARWANDA
@app.get("/webhook/pindo")
def query_speech_rw() -> dict:
    print(request)
    return {"Hello": "World"}

#SPEECH ENABLED QUERY KINYARWANDA
@app.post("/query/speech/rw")
def query_speech_rw() -> dict:
    print(request)
    return {"Hello": "World"}

#SPEECH ENABLED QUERY ENGLISH
@app.post("/query/speech/en")
def query_speech_en() -> dict:
    print(request)
    return {"Hello": "World"}

#TEXT BASED QUERY KINYARWANDA
@app.post("/query/text/rw")
def query_text_rw() -> dict:
    print(request.args.get("mobile"))
    print(request.args.get("query"))
    return {"Query": request.args.get("query"),
            "mobile": request.args.get("mobile")
    }

#TEXT BASED QUERY ENGLISH
@app.post("/query/text/en")
def query_text_en() -> dict:
    print(request.args.get("mobile"))
    print(request.args.get("query"))
    return {"Query": request.args.get("query"),
            "mobile": request.args.get("mobile")
    }


if __name__ =='__main__':  
    app.run(debug = True) 