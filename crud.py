from sqlalchemy.orm import Session
from models import Notification


def create_notification(db: Session, title: str, chapter: str, chapter_url: str, image_url: str):
    notification = Notification(
        title=title,
        chapter=chapter,
        chapter_url=chapter_url,
        image_url=image_url,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def sync_read_status(db: Session):
    db.query(Notification).filter_by(it_was_read=False).update({"it_was_read": True})

def get_unread_notifications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Notification).filter_by(it_was_read=False).offset(skip).limit(limit).all()

def mark_notification_as_read(db: Session, notification_id: int):
    notification = db.query(Notification).filter_by(id=notification_id).first()
    if notification:
        notification.it_was_read = True
        db.commit()
    return notification

def is_notification_duplicate(db: Session, title: str, chapter: str):
    return db.query(Notification).filter_by(title=title, chapter=chapter).first() is not None

    
