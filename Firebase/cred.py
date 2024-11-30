import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    # Check if Firebase app is already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
        'storageBucket': 'colossus-726c5.appspot.com'
        })
    
    # Return Firestore client
    db = firestore.client()
    return db
