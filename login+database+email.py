import json
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path
from email.message import EmailMessage

# from firebase_auth import Auth

def connection_with_firebase():
    global db
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


def entering_marks_in_firebase():
    
    with open("marks_converted.json", "r") as f:
        data = json.load(f)
    
    
    
    for item in data:
        # Convert the dictionary to a Firestore document
        doc = {key: value for key, value in item.items()}

        # Get the Sr. No. from the document and use it as the document ID
        sr_no = doc.get('Sr No')  # Replace 'Sr. No.' with the actual key in the dictionary

        # Add the document to the collection using the Sr. No. as the document ID
        main_collection = db.collection('users').document('7CuCmt3kZYdc1NurpLVnWDe6tPf1')
        collection = main_collection.collection("Marks Records")
        collection.document(sr_no).set(doc)
        
    send_email()
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
    
    
def send_email():
    dotenv_path = Path("./.env")
    load_dotenv(dotenv_path=dotenv_path)
    PASSWORD = os.getenv("PASSWORD")

    # Create SMTP session
    s = smtplib.SMTP("smtp.gmail.com", 587)

    # Start TLS for security
    s.starttls()

    # Authentication
    EMAIL_ADDRESS = "no.reply.result.update@gmail.com"  # Replace with your email address
    s.login(EMAIL_ADDRESS, PASSWORD)

    # Create an EmailMessage object
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "ishpuneetsingh6@gmail.com"  # Replace with the recipient's email address
    msg["Subject"] = "Result Update"  # Add the subject to the email

    # Set the email body
    msg.set_content("There is change in your marks on webkiosk")

    # Sending the email
    s.send_message(msg)
    print("Email sent successfully!")

    # Terminate the session
    s.quit()


if __name__ == "__main__":
    
    connection_with_firebase()
    
    # sign_up_with_email_and_password(email, password, phone_number, roll_number)
    
    # print(sign_in_with_email_and_password('new_user@example.com','new_user_password'))
    
    # entering_marks_in_firebase()
    with open("marks_converted.json", "r") as f:
        data = json.load(f)
        
    user_details = get_user_details('7CuCmt3kZYdc1NurpLVnWDe6tPf1')
    if len(user_details)<len(data):
        entering_marks_in_firebase()
    else:
        print("No New Record Found")
    # print(len(user_details))
    
    # for i in user_details:
    #     print(i)
    #     print()
    
    
    # main()