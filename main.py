from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {
        'name':"rasindu"
    }
@app.get('/about')
def index():
    return {
        'name':"rasindu"
    }