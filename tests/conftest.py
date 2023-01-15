import os
import tempfile
import pytest
import models
from flask_sqlalchemy import SQLAlchemy
from api import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../tests/test_database.db"
    db.init_app(app)

    with app.app_context():  
        db.create_all()
        yield app
        db.session.remove()  
        db.drop_all()



