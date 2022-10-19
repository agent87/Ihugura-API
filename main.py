import sys
from flask import Flask, request
from packages import pindo, stt
from packages.translate import translator, trans_prediction
import json
#Haystack dependencies
import os
import re
from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import clean_wiki_text, convert_files_to_docs
from haystack.nodes import TfidfRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {}




document_store = InMemoryDocumentStore()



#docs = convert_files_to_docs(dir_path="docs/", split_paragraphs=True)
with open("docs/code_of_criminal_procedures.txt", "rb") as f:
    text = re.sub('\t', '',f.read().decode('utf-8'))

dicts = [{"content": text, 'meta': {'name': 'code_of_criminal_procedures'}}]

document_store.write_documents(dicts)


# Load a  local model or any of the QA models on
# Hugging Face's model hub (https://huggingface.co/models)



retriever = TfidfRetriever(document_store=document_store)

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)


pipe = ExtractiveQAPipeline(reader, retriever)



#Start the app
app = Flask(__name__)


#Import Config
app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')


#INDEX
@app.route("/")
def root():
    return 'Welcome to the Ihugure Chatbot API!'

#SPEECH ENABLED QUERY KINYARWANDA
@app.route("/webhook/pindo")
def webhook_pindo() -> dict:
    print(request)
    return True

#SPEECH ENABLED QUERY KINYARWANDA
@app.route("/query/speech/rw", methods=['POST'])
def query_speech_rw() -> dict:
    text_query = stt.convert.to_text(request.files['query'] ) #SPEECH TO TEXT CONVERSION
    query_en = translator.to_en(text_query)
    prediction = pipe.run(query=query_en + "?", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    return {'prediction' : trans_prediction(prediction), 'speech_query':text_query}

#SPEECH ENABLED QUERY ENGLISH
@app.route("/query/speech/en", methods=['POST'])
def query_speech_en() -> dict:
    speech_file = request.files['query']  #ENG AUDIOFILE
    return "English Speech is currently unavailable!"

#TEXT BASED QUERY KINYARWANDA
@app.route("/query/text/rw", methods=['POST'])
def query_text_rw() -> dict:
    query_en = translator.to_en(request.args.get("query"))
    prediction = pipe.run(query=query_en + "?", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    return trans_prediction(prediction)
    

#TEXT BASED QUERY ENGLISH
@app.route("/query/text/en", methods=['POST'])
def query_text_en() -> dict:
    prediction = pipe.run(query=request.args.get("query") + "?", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    return trans_prediction(prediction)
    

if __name__ =='__main__':  
    app.run(debug = True) 