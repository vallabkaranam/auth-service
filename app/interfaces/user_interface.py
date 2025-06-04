from typing import List
from sqlalchemy.orm import Session

from app.db.models.user_models import User
from app.schemas.auth_schemas import SignupUserRequest

class UserInterface:
    """
    Data access interface for user-related database operations.
    Provides a clean abstraction layer between controllers and database models.
    """
    def __init__(self, db: Session):
        """
        Initialize with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the database.
        
        Returns:
            List[User]: List of all user records
        """
        return self.db.query(User).all()
    
    def get_user_by_email(self, email: str) -> User | None:
        """
        Finds a user by their email address.
        
        Args:
            email: User's email address
            
        Returns:
            User | None: User record if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
        
    def create_user(self, email: str, hashed_password: str, first_name: str, last_name: str) -> User:
        """
        Creates a new user record in the database.
        
        Args:
            email: User's email address
            hashed_password: Bcrypt-hashed password
            first_name: User's first name
            last_name: User's last name
            
        Returns:
            User: Created user record
        """
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
