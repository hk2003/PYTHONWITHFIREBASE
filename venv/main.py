import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load Firebase service account key
cred = credentials.Certificate("C:/Users/kumar/Downloads/PythonWithFireBase/venv/firebase_config.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://harsu--002-default-rtdb.firebaseio.com/'
})

app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Function to extract data from Excel
def extract_data(file_path):
    df = pd.read_csv(file_path)
    data = df.to_dict(orient='records')
    return data

# Function to store data in Firebase
def store_data_in_firebase(data):
    ref = db.reference("dataset")
    ref.set(data)
    print("Data uploaded to Firebase!")

# Load data and store it
file_path = "C:/Users/kumar/Downloads/PythonWithFireBase/venv/Data.csv"
extracted_data = extract_data(file_path)
store_data_in_firebase(extracted_data)

# API Endpoint to fetch data from Firebase
@app.get("/data")
def get_data():
    ref = db.reference("dataset")
    data = ref.get()
    return {"data": data}
