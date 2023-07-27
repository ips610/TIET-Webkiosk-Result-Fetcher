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
# Get a reference to the root of the Firebase Realtime Database
# root_ref = db.reference()

# # Write data to the database
# root_ref.child("users").child("user_id").set({"name": "John", "age": 30})

# # Read data from the database
# snapshot = root_ref.child("users").child("user_id").get()
# print(snapshot.val())
print("DONE")



# def sign_in_with_email_and_password(email, password, phone_number, roll_number):
#     try:
#         # Sign in the user with email and password
#         user = auth.get_user_by_email(email)
#         # You can also verify the password by calling auth.verify_password() method
#         # auth.verify_password(user.uid, password)

#         # If successful, return the user UID
#         return user.uid
#     except auth.AuthError as e:
#         # Handle sign-in errors
#         error_code = e.code
#         error_message = e.message
#         print("Sign-in error:", error_code, "-", error_message)
#         return None

# # Example usage:
# email = "user@example.com"
# password = "user_password"
# user_id = sign_in_with_email_and_password(email, password)
# if user_id:
#     print(f"User signed in successfully. UID: {user_id}")
# else:
#     print("Sign-in failed.")


def sign_up_with_email_and_password(email, password, phone_number, roll_number):
    try:
        # Create a new user with email and password
        user = auth.create_user(email=email, password=password)

        # If successful, return the newly created user UID
        db.collection("users").document(user.uid).set({
            "roll": roll_number,
            "phone": phone_number
        })
        return True
    except auth.AuthError as e:
        # Handle sign-up errors
        error_code = e.code
        error_message = e.message
        print("Sign-up error:", error_code, "-", error_message)
        return False



email = "new_user@example.com"
password = "new_user_password"
roll=102203100
phone=9876185427
user_id = sign_up_with_email_and_password(email, password, phone, roll)
if user_id:
    print(f"User signed up successfully. UID: {user_id}")
else:
    print("Sign-up failed.")