import enum
from sqlalchemy import Column, Enum as DBEnum, Integer, String
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"  
    USER = "USER" 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(
        DBEnum(UserRole, name="userrole"), # Using DBEnum
        nullable=False,                 
        default=UserRole.USER,             # Python-side default
        server_default=UserRole.USER.value   # Database-level default
    )