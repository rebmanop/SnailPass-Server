from .base import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    master_password_hash = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.String(100), nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    records = db.relationship("Record", cascade="all,delete", backref="user")
    notes = db.relationship("Note", cascade="all, delete", backref="user")

    def __repr__(self):
        return (
            f"\n***User***\n"
            f"id: {self.id}\n"
            f"email: {self.email}\n"
            f"master_password_hash: {self.master_password_hash}\n"
            f"hint: {self.hint}"
            f"\n***User***"
        )
