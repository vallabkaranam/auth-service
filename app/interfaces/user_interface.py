from typing import List
from sqlalchemy.orm import Session

from app.db.models.user_models import User
from app.schemas.auth_schemas import SignupUserRequest

class UserInterface:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
        
    def create_user(self, email: str, hashed_password: str, first_name: str, last_name: str) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
