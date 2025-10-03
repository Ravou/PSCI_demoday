import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
        # Logic to save the model instance to the database
        pass

    def to_dict(self):
        # Return attributes as a dictionary
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }   
    def delete(self):
        # Logic to delete the model instance from the database
        pass