from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_notification, get_unread_notifications, is_notification_duplicate, mark_notification_as_read
from database import Base, engine
from models import Notification
from MangaNotic import fetch_manga_updates
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/update-notifications")
def update_notifications(db: Session = Depends(get_db)):
    try:
        manga_data = fetch_manga_updates()  # Obter dados da função
        new_notifications = []
        
        for manga in manga_data:
            if not is_notification_duplicate(db, manga["title"], manga["chapter"]):
                new_notification = create_notification(
                    db,
                    title=manga["title"],
                    chapter=manga["chapter"],
                    chapter_url=manga["chapter_url"],
                    image_url=manga["image_url"],
                )
                new_notifications.append(new_notification)
        
        return {"success": True, "new_notifications": new_notifications}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/unread-notifications")
def list_unread_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_unread_notifications(db, skip, limit)

@app.get("/read-notifications")
def list_read_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Notification).filter_by(it_was_read=True).offset(skip).limit(limit).all()


@app.put("/mark-as-read/{notification_id}")
def mark_as_read(notification_id: int, db: Session = Depends(get_db)):
    notification = mark_notification_as_read(db, notification_id)
    if notification:
        return {"success": True, "message": "Notification marked as read"}
    else:
        return {"success": False, "message": "Notification not found"}

@app.post("/sync-read-status")
def sync_read_status(db: Session = Depends(get_db)):
    try:
        manga_data = fetch_manga_updates()  
        titles_with_chapters = {(m["title"], m["chapter"]) for m in manga_data}

        unread_notifications = db.query(Notification).filter_by(it_was_read=False).all()
        
        updated_count = 0
        for notification in unread_notifications:
            if (notification.title, notification.chapter) not in titles_with_chapters:
                notification.it_was_read = True
                updated_count += 1

        db.commit()
        return {"success": True, "updated_count": updated_count}
    except Exception as e:
        return {"success": False, "error": str(e)}
