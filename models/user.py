from google.oauth2 import service_account
from google.cloud import firestore
from datetime import datetime
import os

# Load the service account key file into a credentials object
path_to_credentials = os.path.join(os.path.dirname(__file__), '../config/conversation-ai-39130-01e699d05091.json')
credentials = service_account.Credentials.from_service_account_file(path_to_credentials)

# Create a Firestore client using the credentials object
db = firestore.Client(credentials=credentials)

# Description for the User class
# This class represents a user in the database and provides methods for interacting with the database and the user object. 

class User:
    def __init__(self, id=None, email=None, password=None, created_at=None, updated_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    # Example usage: 
    # user = User()
    # user.email = '
    # user.password = 'password'
    # user.save()
    def save(self):
        now = datetime.now()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        if not self.id:
            doc_ref = db.collection('users').document()
            self.id = doc_ref.id
        else:
            doc_ref = db.collection('users').document(self.id)
        doc_ref.set(self.to_dict())

    # Example usage:
    # user = User.get_by_id('123')
    # user.delete()
    def delete(self):
        if self.id:
            db.collection('users').document(self.id).delete()

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @staticmethod
    def from_dict(doc_dict):
        user = User()
        user.id = doc_dict.get('id')
        user.email = doc_dict.get('email')
        user.password = doc_dict.get('password')
        user.created_at = doc_dict.get('created_at')
        user.updated_at = doc_dict.get('updated_at')
        return user

    @staticmethod
    def get_by_id(user_id):
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return User.from_dict(doc.to_dict())
        else:
            return None

    @staticmethod
    def get_by_email(email):
        users_ref = db.collection('users').where('email', '==', email).limit(1).get()
        for doc in users_ref:
            return User.from_dict(doc.to_dict())
        return None
