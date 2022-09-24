from fastapi import FastAPI
from packages import pindo

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

