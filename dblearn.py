import firebase_admin
from firebase_admin import credentials, firestore, auth



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

document = db.collection('test').document('testing')
document.set({
    'first child': {
        'name': 'John Doe',
        'age': 30
        }
    })

print("Done")