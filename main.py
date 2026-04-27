from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello():
    return 'hello'


@app.get('/about')
def about():
    return"this is about"
