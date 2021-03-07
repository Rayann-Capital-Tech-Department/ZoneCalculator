from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.pickle.

# Step 1: The ID of the spreadsheets
ingredientSheet_ID = '1FihBuWgOUalxuA_b77RPCXoSEgr3Crcrt1MHAH4ts1I'
inputListSheet_ID = '1PAx65UAcSWvHb9_cs2h4ooGFjgfKY_mhjGAcB8Ic_4E'
outputListSheet_ID = '1g10_SjiUuvz9am2ADL7yzOZfREGAtP-Jy8NumTt4RzI'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
