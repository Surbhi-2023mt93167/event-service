from database import db
import uuid

class Event(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    organizer_id = db.Column(db.String, nullable=False)
