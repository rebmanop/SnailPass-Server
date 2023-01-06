from api import db
        

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
      return f"id: {self.id}, email: {self.email}"


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
        return f"id: {self.id}, encrypted_password: {self.encrypted_password}, user_id: {self.user_id}"


class AdditionalField(db.Model):
    __tablename__ = "additional_fields"


    id = db.Column(db.String, primary_key=True)
    field_name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    nonce = db.Column(db.String, nullable=False)
    
    record_id = db.Column(db.String, db.ForeignKey('records.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"id: {self.id}, field_name: {self.field_name}, value: {self.value}, record_id: {self.record_id}"


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
        return f"id: {self.id}, name: {self.name}, content: {self.content}, user_id: {self.user.id}"


#db.drop_all()
#db.create_all()






