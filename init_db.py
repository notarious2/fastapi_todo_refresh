from database import engine, Base
from config import settings

Base.metadata.create_all(bind=engine)
