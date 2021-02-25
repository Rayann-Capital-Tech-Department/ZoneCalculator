from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.pickle.

# Step 1: The ID of the spreadsheets
ingredientSheet_ID = '1VkSVE1wUSWzIL6tL7iz9D4fsSvkgSY7svvwkmLb9_e0'
inputListSheet_ID = '1ecMsdBj8GK1HL2ps-ouV0Zu3fqLD-BYmCylM5KZb_MA'
outputListSheet_ID = '1fV96CIiY57L4Xje0Kr7BLIwt0Gjoyuq1B4-mpIamkVk'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
