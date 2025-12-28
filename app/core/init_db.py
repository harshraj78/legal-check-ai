from app.core.db import engine
from app.models.base import Base

def init_db():
    Base.metadata.create_all(bind=engine)
