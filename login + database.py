import json
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
# from firebase_auth import Auth

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

def connection_with_firebase():
    global db
    
    db = firestore.client(default_app)
    print("Connected With Firebase")


def sign_up_with_email_and_password(email, password, phone_number, roll_number):
    try:
        # Create a new user with email and password
        user = auth.create_user(email=email, password=password)

        # If successful, return the newly created user UID
        db.collection("users").document(user.uid).set(
            {"roll": roll_number, "phone": phone_number}
        )

        return True

    except auth.AuthError as e:
        # Handle sign-up errors
        error_code = e.code
        error_message = e.message

        print("Sign-up error:", error_code, "-", error_message)

        return False


# async def sign_in_with_email_and_password(email, password):
#     global user_uid
#     try:
#         # Sign in the user with email and password
#         credential = auth.EmailAuthProviderAsync.credential_from_email_password(email, password)
#         user = await auth.sign_in_with_credential_async(credential)
#         user_uid = user.uid
#         return user_uid
#     except Exception as e:
#         # Handle all other errors
#         print(f"Error: {e}")

# Function for signing in with email and password
def sign_in_with_email_and_password(email, password):
    try:
        # Sign in the user with email and password
        user = auth.get_user_by_email(email)  # Fetch the user's data
        user_uid = user.uid

        # Sign in the user
        auth_user = auth.get_user(user_uid)

        # Authenticate the user using their email and password
        auth_user = auth.update_user(
            user_uid,
            email=email,
            password=password,
        )

        # Return the user UID if authentication is successful
        return auth_user.uid

    except auth.AuthError as e:
        # Handle sign-in errors
        error_code = e.code
        error_message = e.detail

        print("Sign-in error:", error_code, "-", error_message)
        return None


def entering_marks_in_firebase():
    
    with open("marks_converted.json", "r") as f:
        data = json.load(f)
    
    for item in data:
        # Convert the dictionary to a Firestore document
        doc = {key: value for key, value in item.items()}

        # Get the Sr. No. from the document and use it as the document ID
        sr_no = doc.get('Sr No')  # Replace 'Sr. No.' with the actual key in the dictionary

        # Add the document to the collection using the Sr. No. as the document ID
        main_collection = db.collection('users').document('fYHjyQ6st0Uq4YKjpsv6Zk5qoup1')
        collection = main_collection.collection("Marks Records")
        collection.document(sr_no).set(doc)
    print("Marks Entered")
    
    
def get_user_details(user_uid):
    try:
        # Get the user details from the Firebase database
        db = firestore.client()
        # Create a reference to the "Marks Records" collection for the specific user
        marks_collection_ref = db.collection("users").document(user_uid).collection("Marks Records")

        # Query all documents from the collection
        marks_records = marks_collection_ref.get()

        # Sort the documents based on the "sr no" value inside each document
        sorted_marks_records = sorted(marks_records, key=lambda doc: doc.to_dict().get("sr no", 0))
        
        return [doc.to_dict() for doc in marks_records]

        # Check if the document exists
        if user_data.exists:
            # Return the user details as a dictionary
            return user_data.to_dict()
        else:
            # Handle the case when the user does not exist
            return None
    except Exception as e:
        # Handle any other exceptions that may occur during the retrieval
        print("Error fetching user details:", e)
        return None


# async def main():
#     user_uid = await sign_in_with_email_and_password('new_user@example.com','new_user_password')
#     print(user_uid)
    

if __name__ == "__main__":
    
    connection_with_firebase()
    
    # Call your sign-up function if needed
    # sign_up_with_email_and_password(email, password, phone_number, roll_number)
    
    # Call the sign-in function
    email = "new_user@example.com"
    password = "new_user_password"
    user_uid = sign_in_with_email_and_password(email, password)
    
    if user_uid:
        print("User signed in with UID:", user_uid)
        
        # Perform other operations after signing in
        entering_marks_in_firebase()
        
        user_details = get_user_details(user_uid)
        
        print(len(user_details))
        
        for i in user_details:
            print(i)
            print()
    
    else:
        print("Sign-in failed.")

    
    # main()