# backend/app/models/task.py
from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority
        }
