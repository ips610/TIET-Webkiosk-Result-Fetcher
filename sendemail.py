from __future__ import print_function

import base64
from email.message import EmailMessage
from google.oauth2 import service_account
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmail_send_message():
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = service_account.Credentials.from_service_account_file(
        "IPS.json", scopes=["https://www.googleapis.com/auth/gmail.send"]
    )

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content("This is automated draft mail")

        message["To"] = "ishpuneetsingh610@gmail.com"
        message["From"] = "ishpuneetsingh6@gmail.com"
        message["Subject"] = "Automated draft"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message


if __name__ == "__main__":
    gmail_send_message()
