from flask_migrate import Migrate
from api import create_app
from api.models import db


app = create_app()


migrate = Migrate(app, db)


@app.cli.command("recreate_db")
def recreate_db():
    """
    Recreates a database. This should only be used once
    when there's a new database instance. This shouldn't be
    used when you migrate your database.
    If you will use it on an existing database all data will be lost.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
