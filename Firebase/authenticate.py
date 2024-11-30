import requests
from dotenv import load_dotenv
load_dotenv()
import os

def authenticate_ngo(email, password):

    FIREBASE_API_KEY=os.getenv("FIREBASE_API_KEY")
    
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        id_token = response.json()['idToken']
        return id_token
    else:
        return None

def create_user(email, password):
    FIREBASE_API_KEY=os.getenv("FIREBASE_API_KEY")
    
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        id_token = response.json()['idToken']
        return id_token
    else:
        return None
    