import json
import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account
from google.cloud import firestore
import os

# Load the credentials from the environment variable
firestore_credentials = os.environ.get("FIRESTORE_CREDENTIALS_JSON")

creds_dict = json.loads(firestore_credentials)

# Create a credentials object from the dictionary
creds = service_account.Credentials.from_service_account_info(creds_dict)
app = firebase_admin.initialize_app(credential=credentials.Certificate(creds_dict))

# Initialize the Firestore client with the credentials
db = firestore.Client(credentials=creds)
