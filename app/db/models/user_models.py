import enum
from sqlalchemy import Column, Enum as DBEnum, Integer, String
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    """
    Enumeration of possible user roles in the system.
    Used for role-based access control (RBAC).
    """
    ADMIN = "ADMIN"  # Users with administrative privileges
    USER = "USER"    # Regular users with standard access

class User(Base):
    """
    SQLAlchemy model representing a user in the system.
    
    Attributes:
        id (int): Primary key, auto-incrementing user ID
        email (str): Unique email address used for authentication
        hashed_password (str): Bcrypt-hashed password
        first_name (str): User's first name
        last_name (str): User's last name
        role (UserRole): User's role in the system (ADMIN or USER)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(
        DBEnum(UserRole, name="userrole"), # Using DBEnum for type safety
        nullable=False,                 
        default=UserRole.USER,             # Python-side default
        server_default=UserRole.USER.value   # Database-level default
    )