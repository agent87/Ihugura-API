from fastapi import FastAPI, File
from packages import pindo

app = FastAPI()

#INDEX
@app.get("/")
def root():
    return {"Hello": "World"}

#SPEECH ENABLED QUERY KINYARWANDA
@app.post("/query/speech/rw")
def query_voice_rw() -> dict:
    return {"Hello": "World"}

#SPEECH ENABLED QUERY ENGLISH
@app.post("/query/speech/en")
def query_voice_rw() -> dict:
    return {"Hello": "World"}

#TEXT BASED QUERY KINYARWANDA
@app.post("/query/text/rw")
def query_voice_rw(query: str, mobile: str) -> dict:
    print(query, mobile)
    return {"Hello": "World"}

#TEXT BASED QUERY ENGLISH
@app.post("/query/text/en")
def query_voice_rw(query: str) -> dict:
    return {"Hello": "World"}