from .base import db


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(
        db.String, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    is_favorite = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return (
            f"\n***Note***\n"
            f"id: {self.id}\n"
            f"name: {self.name}\n"
            f"content: {self.content}\n"
            f"user_id: {self.user_id}\n"
            f"is_favorite: {self.is_favorite}\n"
            f"is_deleted: {self.is_deleted}\n"
            f"creation_time: {self.creation_time}\n"
            f"update_time: {self.update_time}"
            f"\n***Note***"
        )
