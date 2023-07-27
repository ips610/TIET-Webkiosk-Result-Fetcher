import firebase_admin
from firebase_admin import credentials, firestore, auth
import json


cred = credentials.Certificate("./ru.json")
default_app = firebase_admin.initialize_app(
    cred,
    {
        "apiKey": "AIzaSyB3EDMY_ANLh6vqC_LwhLmLhbw_okePfjo",
        "authDomain": "result-update-626.firebaseapp.com",
        "projectId": "result-update-626",
        "storageBucket": "result-update-626.appspot.com",
        "messagingSenderId": "217810071418",
        "appId": "1:217810071418:web:7f34572f6a076855fc30c3",
        "measurementId": "G-7LKBG4GB93",
    },
)
db = firestore.client(default_app)

collection = db.collection('test')
# document.set({
#     'first child': {
#         'name': 'John Doe',
#         'age': 30
#         }
#     })

with open("marks_converted.json", "r") as f:
    data = json.load(f)
    
for item in data:
    # Convert the dictionary to a Firestore document
    doc = {key: value for key, value in item.items()}

    # Add the document to the collection
    collection.add(doc)
    
print("Done")