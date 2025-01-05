from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    chapter = Column(String, index=True)
    chapter_url = Column(String)
    image_url = Column(String)
    it_was_read = Column(Boolean, default=False)
