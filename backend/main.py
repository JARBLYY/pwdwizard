from fastapi import FastAPI
from PWDWizard.SavingAndRetrieving import save_password, get_passwords
from PWDWizard.MasterPassword import get_key_from_password
from PWDWizard.ProtectMasterAndSalt import load_or_create_salt

app = FastAPI()

@app.get("/")
def home():
    return {"message": "pwdwizard backend is runningggggg test test test"} 

@app.get("/test-db")
def database_test():

    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="password",
        database="pwdwizard"
    )

    return {"database": "works"}