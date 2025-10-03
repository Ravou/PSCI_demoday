from .base import BaseModel

class User(BaseModel):
    def __init__(self, name: str, email: str, password_hash: str):
        super().__init__()
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password: str) -> bool :
        # Logic to check password validity
        pass

    def update_email(self, new_email: str):
        self.email = new_email
        # Logic to send confirmation email

    def get_profile(self) -> dict:
        # Return a  dictionary with user profile information
        return {
            "name": self.name,
            "email": self.email,
            "id": str(self.id),
        }