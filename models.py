from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#db.metadata.clear()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    master_password_hash = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    records = db.relationship("Record", cascade="all,delete", backref="user") 

    def __repr__(self):
      return (
                f'\n***User***\n'
                f'id: {self.id}\n'
                f'email: {self.email}\n'
                f'master_password_hash: {self.master_password_hash}\n'
                f'hint: {self.hint}\n'
                f'is_admin: {self.is_admin}'
                f'\n***User***'
                )


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
    nonce = db.Column(db.String, nullable=False)
    
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
                f'nonce: {self.nonce}'
                f'\n***Record***'
                )

class AdditionalField(db.Model):
    __tablename__ = "additional_fields"


    id = db.Column(db.String, primary_key=True)
    field_name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    nonce = db.Column(db.String, nullable=False)
    
    record_id = db.Column(db.String, db.ForeignKey('records.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
              return (
                f'\n***Additional Field***\n'
                f'id: {self.id}\n'
                f'field_name: {self.field_name}\n'
                f'value: {self.value}\n'
                f'nonce: {self.nonce}\n'
                f'record_id: {self.record_id}'
                f'\n***Additional Field***'
                )


class Note(db.Model):
    __tablename__ = "notes"
                                            
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    nonce = db.Column(db.String, nullable=False)

    def __repr__(self):
               return (
                f'\n***Note***\n'
                f'id: {self.id}\n'
                f'name: {self.name}\n'
                f'content: {self.content}\n'
                f'user_id: {self.user_id}\n'
                f'is_favorite: {self.is_favorite}\n'
                f'is_deleted: {self.is_deleted}\n'
                f'creation_time: {self.creation_time}\n'
                f'update_time: {self.update_time}\n'
                f'nonce: {self.nonce}'
                f'\n***Note***'
                )


#db.drop_all()
#db.create_all()






