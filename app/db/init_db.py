from app.db.base import Base, engine
from app.db.models.user_models import User

# Create all tables
Base.metadata.create_all(bind=engine)