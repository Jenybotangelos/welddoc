from app.database import db


class Client(db.Model):
    __tablename__ = "weldoc_clients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    street = db.Column(db.String(200))
    zip_code = db.Column(db.String(20))
    location = db.Column(db.String(200))
    remarks = db.Column(db.Text)
    archived = db.Column(db.Boolean, default=False)

    projects = db.relationship("Project", backref="client", lazy=True)
