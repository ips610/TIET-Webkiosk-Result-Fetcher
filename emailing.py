import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path("./.env")
load_dotenv(dotenv_path=dotenv_path)
PASSWORD = os.getenv("PASSWORD")
# creates SMTP session
s = smtplib.SMTP("smtp.gmail.com", 587)

# start TLS for security
s.starttls()

# Authentication
s.login("ishpuneetsingh6@gmail.com", PASSWORD)

# message to be sent
message = "Hello"

# sending the mail
s.sendmail("ishpuneetsingh6@gmail.com", "muskanchalana.26@gmail.com", message)
print("SENT")
# terminating the session
s.quit()
