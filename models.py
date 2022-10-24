from api import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    master_password_hash = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    nonce = db.Column(db.String, nullable=False)
    
    records = db.relationship('Record', backref='user', lazy=True) 

    def __repr__(self):
      return f"id: {self.id}, email: {self.email}"


class Record(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    login = db.Column(db.String, nullable=False)
    encrypted_password = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    
    additional_fields = db.relationship('AdditionalField', backref='record', lazy=True)

    def __repr__(self):
        return f"id: {self.id}, encrypted_password: {self.encrypted_password}, user_id: {self.user_id}"


class AdditionalField(db.Model):
    id = db.Column(db.String, primary_key=True)
    field_name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    
    record_id = db.Column(db.String, db.ForeignKey('record.id'), nullable=False)

    def __repr__(self):
        return f"id: {self.id}, field_name: {self.field_name}, value: {self.value}, record_id: {self.record_id}"




