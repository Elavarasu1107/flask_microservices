from sqlalchemy import inspect
from core import db


class Label(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, index=True)
    name = db.Column(db.String(150))
    color = db.Column(db.String(150))
    user_id = db.Column(db.BigInteger, nullable=False)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __str__(self):
        return f'{self.name}'
