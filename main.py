import sys
print(sys.executable)
from flask import Flask, request
from packages import pindo, stt
from packages.translate import translator
import json
from haystack.file_converter import PDFToTextConverter
from haystack.preprocessor import PreProcessor
from haystack.document_stores.faiss import FAISSDocumentStore
from haystack.retriever import DensePassageRetriever
from haystack.reader import FARMReader
from haystack.pipeline import ExtractiveQAPipeline

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {}



pdf_converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
converted = pdf_converter.convert(file_path = "docs\Justice_for_Children_Policy.pdf", meta = { "company": "Company_1", "processed": False })


#Preprocessing
preprocessor = PreProcessor(split_by="word",
 split_length=200,
 split_overlap=10)
preprocessed = preprocessor.process(converted)


#Create document store
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", return_embedding=True)
document_store.delete_all_documents()
document_store.write_documents(preprocessed)


#Embendings
retriever = DensePassageRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2-distilled", use_gpu=False)
document_store.update_embeddings(retriever)


#Create Pipeline
pipeline = ExtractiveQAPipeline(reader, retriever)



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