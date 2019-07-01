from abc import ABC, abstractmethod
from firebase_admin import firestore


class Entity(ABC):

    def __init__(self, db=None, collection=None):
        self.id = None
        self.db = db
        self.collection = collection
        self.ref = None

    @abstractmethod
    def to_dict(self):
        pass

    def post_action(self, batch=None):
        pass

    def pre_action(self, batch=None):
        pass

    def save(self, db: firestore, batch):
        self.pre_action(batch)
        self.ref = db.collection(self.collection).document()
        self.id = self.ref.id
        # doc.set(self.to_dict())
        batch.set(self.ref, self.to_dict())
        self.post_action(batch)
        return self.ref
