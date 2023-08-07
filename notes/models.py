from sqlalchemy import inspect
from core import db
from sqlalchemy_utils.types import ChoiceType


class Notes(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, index=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(150))
    reminder = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.BigInteger, nullable=False)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __str__(self):
        return f'{self.title}'


class Collaborator(db.Model):
    access = [
        ('writable', 'WRITABLE'),
        ('read_only', 'READ-ONLY')
    ]

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    note_id = db.Column(db.BigInteger, nullable=False)
    access_type = db.Column(ChoiceType(access), nullable=False)
