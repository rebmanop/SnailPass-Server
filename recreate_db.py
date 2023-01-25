import config
from models import db
from api import create_app

app = create_app(config.DevelopmentConfig())
db.init_app(app)
with app.app_context():
    db.metadata.clear()
    db.drop_all()
    db.create_all()
