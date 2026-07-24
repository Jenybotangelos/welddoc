from app.database import db


class User(db.Model):
    __tablename__ = "weldoc_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    archived = db.Column(db.Boolean, default=False)
