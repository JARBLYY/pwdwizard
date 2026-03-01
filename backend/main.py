from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "pwdwizard backend is runningggggg"} 
    return {"message": "testtestg"} 
    