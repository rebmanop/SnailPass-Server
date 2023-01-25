from .base import db


class Record(db.Model): 
    __tablename__ = "records"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    login = db.Column(db.String, nullable=False)
    encrypted_password = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    
    additional_fields = db.relationship("AdditionalField", cascade="all,delete", backref="record") 

    def __repr__(self):
        return (
                f'\n***Record***\n'
                f'id: {self.id}\n'
                f'name: {self.name}\n'
                f'login: {self.login}\n'
                f'encrypted_password: {self.encrypted_password}\n'
                f'is_favorite: {self.is_favorite}\n'
                f'is_deleted: {self.is_deleted}\n'
                f'creation_time: {self.creation_time}\n'
                f'update_time: {self.update_time}\n'
                f'\n***Record***'
                )

