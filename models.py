from api import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    master_password_hash = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    records = db.relationship('Record', backref='user', lazy=True) 

    def __repr__(self):
      return f"id: {self.id}, login: {self.login}"


class Record(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    encrypted_password = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"id: {self.id}, encrypted_password: {self.encrypted_password}, user_id: {self.user_id}"



