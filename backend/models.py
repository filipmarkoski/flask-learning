from app import db
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid


class Task(db.Model):
    __tablename__ = 'Task'

    ID = db.Column(db.BigInteger, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    Description = db.Column(db.String, nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    DateModified = db.Column(db.DateTime, nullable=True)
    IsActive = db.Column(db.Boolean, nullable=False)
    UUID = db.Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)

    def __repr__(self):
        return f'{self.ID}-{self.Name}'
