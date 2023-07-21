"""
google-api-python-client==1.7.9
google-auth-httplib2==0.0.3
google-auth-oauthlib==0.4.0
pip install gspread oauth2client

"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up credentials
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "tiet-result-fetcher-9ca30d1cd812.json", scope
)
client = gspread.authorize(creds)

# Open the Google Sheets spreadsheet by its title
spreadsheet = client.open("Testing Sheets")
print("Sheet Found")
# Select the worksheet by its title
worksheet = spreadsheet.worksheet("Sheet1")

# Read data from the worksheet
data = worksheet.get_all_values()

# Print the data
for row in data:
    print(row)

'''
pip3 install google-auth-oauthlib
pip3 install gspread
pip3 install gspread oauth2client
'''