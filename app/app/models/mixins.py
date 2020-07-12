from app import db
from datetime import datetime

class PrimaryKeyIdMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class UpdateMixin:
    def update(self, values):
        for k, v in values.items():
            setattr(self, k, v)

class StandardMixins(PrimaryKeyIdMixin,
                     TimestampMixin,
                     UpdateMixin):
    pass
