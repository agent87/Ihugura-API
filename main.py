import sys
print(sys.version)
from flask import Flask, request
from packages import pindo, stt
from packages.translate import translator
import json
#Haystack dependencies
from haystack.utils import launch_es
import time
import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.utils import clean_wiki_text, convert_files_to_docs
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {}


launch_es()
time.sleep(30)



# Get the host where Elasticsearch is running, default to localhost
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
document_store = ElasticsearchDocumentStore(host=host, username="", password="", index="document")



docs = convert_files_to_docs(dir_path="docs/", clean_func=clean_wiki_text, split_paragraphs=True)


print(docs[:3])

# Now, let's write the dicts containing documents to our DB.
document_store.write_documents(docs)


# Load a  local model or any of the QA models on
# Hugging Face's model hub (https://huggingface.co/models)

retriever = BM25Retriever(document_store=document_store)

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)


pipe = ExtractiveQAPipeline(reader, retriever)

prediction = pipe.run(
    query="Who is the father of Arya Stark?", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
)

#Start the app
app = Flask(__name__)


#Import Config
app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')


#INDEX
@app.get("/")
def root():
    return 'Welcome to the Ihugure Chatbot API!'

#SPEECH ENABLED QUERY KINYARWANDA
@app.get("/webhook/pindo")
def webhook_pindo() -> dict:
    print(request)
    return True

#SPEECH ENABLED QUERY KINYARWANDA
@app.post("/query/speech/rw")
def query_speech_rw() -> dict:
    speech_file = request.files['query']  #RW AUDIOFILE
    text_query = stt.convert.to_text(speech_file) #SPEECH TO TEXT CONVERSION
    return {"Query": text_query}

#SPEECH ENABLED QUERY ENGLISH
@app.post("/query/speech/en")
def query_speech_en() -> dict:
    speech_file = request.files['query']  #ENG AUDIOFILE
    return {"Query": 'English'}

#TEXT BASED QUERY KINYARWANDA
@app.post("/query/text/rw")
def query_text_rw() -> dict:
    query_en = translator.to_en(request.args.get("query"))
    return {"Query": query_en,
            "mobile": request.args.get("mobile")
    }

#TEXT BASED QUERY ENGLISH
@app.post("/query/text/en")
def query_text_en() -> dict:
    return {"Query": request.args.get("query"),
            "mobile": request.args.get("mobile")
    }


if __name__ =='__main__':  
    app.run(debug = True) 