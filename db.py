from google.oauth2 import service_account
from google.cloud import firestore
import os

# Load the service account key file into a credentials object
path_to_credentials = os.path.join(os.path.dirname(__file__), '../writegpt-cai-0929acae63bb.json')
credentials = service_account.Credentials.from_service_account_file(path_to_credentials)
print("path_to_credentials: ", path_to_credentials)
# Create a Firestore client using the credentials object
db = firestore.Client(credentials=credentials)