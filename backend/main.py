from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "pwdwizard backend is runningggggg test test test. writing wiritng writing"} 