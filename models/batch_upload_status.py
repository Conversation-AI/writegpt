from datetime import datetime

from helpers.db import db


class BatchUploadStatus:
    def __init__(self, id=None, filename=None, created_at=None, updated_at=None, status=None,
                 url=None, user_id=None):
        self.id = id
        self.filename = filename
        self.created_at = created_at
        self.status = status
        self.updated_at = updated_at
        self.url = url
        self.user_id = user_id

    def save(self):
        now = datetime.now()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
        if not self.id:
            doc_ref = db.collection('batch_upload_status').document()
            self.id = doc_ref.id
        else:
            doc_ref = db.collection('batch_upload_status').document(self.id)
        doc_ref.set(self.to_dict())

    # Example usage:
    # user = User.get_by_id('123')
    # user.delete()
    def delete(self):
        if self.id:
            db.collection('users').document(self.id).delete()

    def to_dict(self):
        return {
            'filename': self.filename, 'created_at': self.created_at, 'updated_at': self.updated_at,
            'status': self.status, 'url': self.url,
            'user_id': self.user_id
        }

    @staticmethod
    def get_by_docId(docID):
        doc_ref = db.collection('batch_upload_status').document(docID)
        doc = doc_ref.get()
        if doc.exists:
            data = BatchUploadStatus.from_dict(doc.to_dict())
            data.id = doc.id
            return data
        else:
            return None

    @staticmethod
    def from_dict(doc_dict):
        upload_status = BatchUploadStatus()
        upload_status.id = doc_dict.get('id')
        upload_status.created_at = doc_dict.get('created_at')
        upload_status.updated_at = doc_dict.get('updated_at')
        upload_status.user_id = doc_dict.get('user_id')
        upload_status.status = doc_dict.get('status')
        upload_status.url = doc_dict.get('url')
        upload_status.filename = doc_dict.get('filename')
        return upload_status
