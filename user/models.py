from sqlalchemy import inspect
from flask_validator import ValidateEmail, ValidateString
from sqlalchemy.orm import validates
from core import db


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, index=True, unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250))
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(150))
    phone = db.Column(db.BigInteger)
    location = db.Column(db.String(150))
    is_superuser = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(cls.email, True, True, "The email is not valid. Please check it")
        ValidateString(cls.username, True, True, "The username type must be string")

    @validates('username')
    def empty_string_to_null(self, key, value):
        return None if isinstance(value, str) and value == '' else value

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != 'password'}

    def __str__(self):
        return f'{self.username}'
