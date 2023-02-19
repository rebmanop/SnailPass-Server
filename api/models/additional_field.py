from .base import db


class AdditionalField(db.Model):
    __tablename__ = "additional_fields"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    record_id = db.Column(
        db.String, db.ForeignKey("records.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return (
            f"\n***Additional Field***\n"
            f"id: {self.id}\n"
            f"name: {self.name}\n"
            f"value: {self.value}\n"
            f"record_id: {self.record_id}"
            f"\n***Additional Field***"
        )
