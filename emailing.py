import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path
from email.message import EmailMessage

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
msg.set_content("Hello")

# Sending the email
s.send_message(msg)
print("Email sent successfully!")

# Terminate the session
s.quit()
