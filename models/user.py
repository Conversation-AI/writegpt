from datetime import datetime
import os

from db import db

class User:
    def __init__(self, id=None, email=None, password=None, created_at=None, updated_at=None, 
             customer_id=None, name=None, billing_status=None, subscription_item_id=None, subscription_id=None):
        self.id = id
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.customer_id = customer_id
        self.name = name
        self.billing_status = billing_status
        self.subscription_item_id = subscription_item_id
        self.subscription_id = subscription_id

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
            'customer_id': self.customer_id,
            'name': self.name,
            'billing_status': self.billing_status,
            'subscription_item_id': self.subscription_item_id,
            'subscription_id': self.subscription_id,
        }

    @staticmethod
    def from_dict(doc_dict):
        user = User()
        user.id = doc_dict.get('id')
        user.email = doc_dict.get('email')
        user.password = doc_dict.get('password')
        user.created_at = doc_dict.get('created_at')
        user.updated_at = doc_dict.get('updated_at')
        user.customer_id = doc_dict.get('customer_id')
        user.name = doc_dict.get('name')
        user.billing_status = doc_dict.get('billing_status')
        user.subscription_item_id = doc_dict.get('subscription_item_id')
        user.subscription_id = doc_dict.get('subscription_id')
        return user

    # get_by_id and get_by_email both need to set the user.id before returning user object.
    @staticmethod
    def get_by_id(user_id):
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            user = User.from_dict(doc.to_dict())
            user.id = doc.id
            return user
        else:
            return None

    @staticmethod
    def get_by_email(email):
        users_ref = db.collection('users').where('email', '==', email).limit(1).get()
        for doc in users_ref:
            user = User.from_dict(doc.to_dict())
            user.id = doc.id
            return user
        return None
    
    @staticmethod
    def get_by_customer_id(customer_id):
        users_ref = db.collection('users').where('customer_id', '==', customer_id).limit(1).get()
        for doc in users_ref:
            user = User.from_dict(doc.to_dict())
            user.id = doc.id
            return user
        return None