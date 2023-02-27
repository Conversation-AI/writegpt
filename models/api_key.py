from datetime import datetime
import secrets
import string
import os

from db import db

def generate_secret_key():
    """Generate a random secret key."""
    return secrets.token_urlsafe(16)

class ApiKey:
    def __init__(self, user_id, secret=None, created_at=None, last_used_at=None):
        self.user_id = user_id
        self.secret = secret or generate_secret_key()
        self.created_at = created_at or datetime.now()
        self.last_used_at = last_used_at

    def save(self):
        api_key_ref = self.get_api_key_ref()
        api_key_ref.set(self.to_dict())

    def delete(self):
        api_key_ref = self.get_api_key_ref()
        api_key_ref.delete()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "secret": self.secret,
            "created_at": self.created_at,
            "last_used_at": self.last_used_at
        }
    
    def update_last_used_at(self):
      self.last_used_at = datetime.now()
      self.save()

    @staticmethod
    def from_dict(api_key_dict):
        return ApiKey(
            user_id=api_key_dict["user_id"],
            secret=api_key_dict["secret"],
            created_at=api_key_dict["created_at"],
            last_used_at=api_key_dict["last_used_at"]
        )

    def get_api_key_ref(self):
        user_ref = db.collection("users").document(self.user_id)
        return user_ref.collection("api_keys").document(self.secret)

    @staticmethod
    def get_by_user_id(user_id):
        query = db.collection("users").document(user_id).collection("api_keys")
        docs = query.get()
        api_keys = []
        for doc in docs:
            api_key_data = doc.to_dict()
            api_key = ApiKey.from_dict(api_key_data)
            api_keys.append(api_key)
        return api_keys

    @staticmethod
    def get_by_secret(secret):
        query = db.collection_group("api_keys").where("secret", "==", secret)
        docs = query.get()
        if len(docs) > 0:
            api_key_data = docs[0].to_dict()
            return ApiKey.from_dict(api_key_data)
        else:
            return None
